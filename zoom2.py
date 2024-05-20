# Server

import socket
import threading
import struct
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import sounddevice as sd
import numpy as np

client2_ip = "localhost"

# Set up server sockets for video and audio
video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
video_server.bind((client2_ip, 12345))
video_server.listen(2)

video_client_socket, addr = video_server.accept()
print(f"Accepted video connection from {addr}")


audio_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
audio_server.bind((client2_ip, 12346))
audio_server.listen(2)

audio_client_socket, addr = audio_server.accept()
print(f"Accepted audio connection from {addr}")


def send_video():
    connection = video_client_socket.makefile('wb')
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
        video_client_socket.close()
        print(f"Connection with {addr} closed.")

def get_video():
    try:
        while True:
            # Receive the size of the incoming frame
            size = struct.unpack('!I', video_client_socket.recv(4))[0]

            # Receive and deserialize the frame
            data = b""
            while len(data) < size:
                packet = video_client_socket.recv(size - len(data))
                if not packet:
                    break
                data += packet

            if not data:
                break

            frame = pickle.loads(data)

            # Update the video panel
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            panel.img = img
            panel.config(image=img)
            panel.image = img

    except Exception as e:
        print(f"Error: {e}")
        root.destroy()


def send_audio():
    connection = audio_client_socket.makefile('wb')
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
        audio_client_socket.close()
        print(f"Connection with {addr} closed.")


# Function to play received audio
def get_audio():
    try:
        while True:
            # Receive the size of the incoming audio data
            size = struct.unpack('!I', audio_client_socket.recv(4))[0]

            # Receive and deserialize the audio data
            data = b""
            while len(data) < size:
                packet = audio_client_socket.recv(size - len(data))
                if not packet:
                    break
                data += packet

            if not data:
                break

            # Play the audio
            audio_data = pickle.loads(data)
            sd.play(audio_data, samplerate=44100, blocking=False)

    except Exception as e:
        print(f"Error: {e}")
        root.destroy()


# GUI setup using Tkinter
root = tk.Tk()
root.title("Video Chat Client")

# Create a label for displaying video frames
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# threads
threading.Thread(target=send_video, daemon=True).start()
threading.Thread(target=get_video, daemon=True).start()
threading.Thread(target=send_audio, daemon=True).start()
threading.Thread(target=get_audio, daemon=True).start()


# Start the Tkinter main loop
root.mainloop()




# import socket
# import threading
# import struct
#
# video_clients_info = {}  # Dictionary to store client addresses
#
# def handle_client_video(video_client_socket):
#     # connection = client.makefile('wb')
#     while True:
#         # Receive the size of the incoming frame
#         size = struct.unpack('!I', video_client_socket.recv(4))[0]
#
#         # Receive and send the frame to the other client
#         data = b""
#         while len(data) < size:
#             remaining_bytes = size - len(data)
#             chunk = video_client_socket.recv(min(remaining_bytes, 4096))
#             if not chunk:
#                 print("Connection closed unexpectedly")
#                 break
#             data += chunk
#
#         for client_socket, _ in video_clients_info.items():
#             if client_socket != video_client_socket:
#                 try:
#                     client_socket.sendall(struct.pack('!I', size))
#                     client_socket.sendall(data)
#                 except Exception as e:
#                     print(f"Error broadcasting video to client: {e}")
#                     video_clients_info.pop(client_socket)  # Remove disconnected client
#                     break
#
# def accept_connections():
#     global video_clients_info
#     while len(video_clients_info) < 2:
#         video_client_socket, addr = video_server.accept()
#         print(f"Accepted video connection from {addr}")
#         video_clients_info[video_client_socket] = addr
#
#     for client_socket, client_addr in video_clients_info.items():
#         other_client_addr = next(addr for sock, addr in video_clients_info.items() if sock != client_socket)
#         client_socket.sendall(other_client_addr.encode())
#
#     threading.Thread(target=handle_client_video, args=(video_client_socket,)).start()
#
# # Set up server socket for video
# video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# video_server.bind(("0.0.0.0", 12345))
# video_server.listen()
#
# accept_connections()

