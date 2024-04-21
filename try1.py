# Server
import socket
import threading
import struct
import pickle
import cv2
import sounddevice as sd
import numpy as np

video_clients = []
audio_clients = []

# Function to handle a single client's video stream
def handle_client_video(client_socket, addr):
    connection = client_socket.makefile('wb')

    try:
        cap = cv2.VideoCapture(0)  # 0 for the default camera

        while True:
            ret, frame = cap.read()

            # Serialize the frame and send it to the client
            data = pickle.dumps(frame)
            size = struct.pack('!I', len(data))
            connection.write(size)
            connection.write(data)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cap.release()
        connection.close()
        client_socket.close()
        print(f"Connection with {addr} closed.")


# Function to handle a single client's audio stream
def handle_client_audio(client_socket, addr):
    connection = client_socket.makefile('wb')

    try:
        while True:
            # Record audio from microphone
            data = sd.rec(44100, channels=2, dtype=np.int16)
            sd.wait()

            # Serialize the audio data and send it to the client
            data_serialized = pickle.dumps(data)
            size = struct.pack('!I', len(data_serialized))
            connection.write(size)
            connection.write(data_serialized)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()
        client_socket.close()
        print(f"Connection with {addr} closed.")


# Set up server sockets for video and audio
video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_server.bind(("0.0.0.0", 12345))
video_server.listen(2)

audio_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_server.bind(("0.0.0.0", 12346))
audio_server.listen(2)

# Main server loop for video
while True:
    video_client_socket, addr = video_server.accept()
    print(f"Accepted video connection from {addr}")
    video_clients.append(video_client_socket)

    audio_client_socket, addr = audio_server.accept()
    print(f"Accepted audio connection from {addr}")
    audio_clients.append(audio_client_socket)

    threading.Thread(target=handle_client_video, args=(video_client_socket, addr)).start()
    threading.Thread(target=handle_client_audio, args=(audio_client_socket, addr)).start()


# import socket
#
#
# listening_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# listening_sock.bind(('127.0.0.1', 8200))

#
# msg, client_address = listening_sock.recvfrom(1024)
# listening_sock.sendto(msg, client_address)
#
# listening_sock.close()


# import cv2
# import numpy as np
# import socket
# import threading
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(("0.0.0.0", 12345))
# server.listen(5)
# print("Server listening on port 12345")
#
# def receive_frames():
#     while True:
#         client_socket, _ = server.accept()
#         data = b""
#
#         while True:
#             packet = client_socket.recv(65536)  # Increased buffer size
#             if not packet:
#                 break
#
#             data += packet
#             img_array = np.frombuffer(data, dtype=np.uint8)
#             frame = cv2.imdecode(img_array, 1)  # 1 for an image with colors
#
#             if frame is not None:
#                 print("Received a frame")
#                 print(frame)
#                 cv2.imshow("Server Video", frame)
#                 cv2.waitKey(1)  # Ensure that the window updates
#
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#
#         client_socket.close()
#
#
# # Start the receive thread
# receive_thread = threading.Thread(target=receive_frames)
# receive_thread.start()
#
# # Add an event loop for the OpenCV window
# while True:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Cleanup code
# server.close()
# cv2.destroyAllWindows()
