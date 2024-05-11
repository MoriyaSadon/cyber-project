# Server

import socket
import threading
import struct

video_clients_info = {}  # Dictionary to store client addresses

def handle_client_video(video_client_socket):
    # connection = client.makefile('wb')
    while True:
        # Receive the size of the incoming frame
        size = struct.unpack('!I', video_client_socket.recv(4))[0]

        # Receive and send the frame to the other client
        data = b""
        while len(data) < size:
            remaining_bytes = size - len(data)
            chunk = video_client_socket.recv(min(remaining_bytes, 4096))
            if not chunk:
                print("Connection closed unexpectedly")
                break
            data += chunk

        for client_socket, _ in video_clients_info.items():
            if client_socket != video_client_socket:
                try:
                    client_socket.sendall(struct.pack('!I', size))
                    client_socket.sendall(data)
                except Exception as e:
                    print(f"Error broadcasting video to client: {e}")
                    video_clients_info.pop(client_socket)  # Remove disconnected client
                    break

def accept_connections():
    global video_clients_info
    while len(video_clients_info) < 2:
        video_client_socket, addr = video_server.accept()
        print(f"Accepted video connection from {addr}")
        video_clients_info[video_client_socket] = addr

    for client_socket, client_addr in video_clients_info.items():
        other_client_addr = next(addr for sock, addr in video_clients_info.items() if sock != client_socket)
        client_socket.sendall(other_client_addr.encode())

    threading.Thread(target=handle_client_video, args=(video_client_socket,)).start()

# Set up server socket for video
video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_server.bind(("0.0.0.0", 12345))
video_server.listen()

accept_connections()



# import socket
# import threading
# import struct
# import pickle
# import cv2
# import sounddevice as sd
# import numpy as np
#
# video_clients = []
# audio_clients = []
#
#
# def handle_client_video():
#     # connection = client.makefile('wb')
#     while True:
#         # Receive the size of the incoming frame
#         size = struct.unpack('!I', video_client_socket.recv(4))[0]
#
#         # Receive and deserialize the frame
#         data = b""
#         while len(data) < size:
#             # Determine the amount of data remaining to be received
#             remaining_bytes = size - len(data)
#             # Receive data in smaller chunks to avoid overflow error
#             chunk = video_client_socket.recv(min(remaining_bytes, 4096))  # Adjust chunk size as needed
#             if not chunk:
#                 # Handle case where connection is closed unexpectedly
#                 print("Connection closed unexpectedly")
#                 break
#             data += chunk
#             if not data:
#                 break
#
#         for client in video_clients:
#             if len(video_clients) > 1 and client != video_client_socket:
#                 data = pickle.dumps(data)
#                 size = struct.pack('!I', len(data))
#                 video_client_socket.sendall(size)
#                 video_client_socket.sendall(data)
#                 # connection.write(size)
#                 # connection.write(data)
#
#
# # Function to handle client's audio stream
# def handle_client_audio(audio_client_socket):
#     try:
#         while True:
#             # Receive the size of the incoming audio data
#             size_data = audio_client_socket.recv(4)
#             if not size_data:
#                 break
#
#             size = struct.unpack('!I', size_data)[0]
#
#             # Receive and deserialize the audio data
#             data = b""
#             while len(data) < size:
#                 packet = audio_client_socket.recv(size - len(data))
#                 if not packet:
#                     break
#                 data += packet
#
#             if not data:
#                 break
#
#             # Broadcast the audio data to other clients
#             for client_socket in audio_clients[:]:  # Iterate over a copy of the list
#                 if client_socket != audio_client_socket and isinstance(client_socket, socket.socket):
#                     try:
#                         client_socket.send("audio".encode())
#                         client_socket.sendall(struct.pack('!I', size))
#                         client_socket.sendall(pickle.loads(data))
#
#                     except Exception as e:
#                         print(f"Error broadcasting audio to client: {e}")
#                         # If an error occurs, assume the client has disconnected and remove it from the list
#                         audio_clients.remove(client_socket)
#
#     except Exception as e:
#         print(f"Error handling audio client: {e}")
#     finally:
#         audio_client_socket.close()
#         # Remove the client's socket from the list after closing the connection
#         if audio_client_socket in audio_clients:
#             audio_clients.remove(audio_client_socket)
#
#
# # Set up server sockets for video and audio
# video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# video_server.bind(("0.0.0.0", 12345))
# video_server.listen()
#
# audio_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# audio_server.bind(("0.0.0.0", 12346))
# audio_server.listen()
#
# # Main server loop for video
# while True:
#     video_client_socket, addr = video_server.accept()
#     print(f"Accepted video connection from {addr}")
#     video_clients.append(video_client_socket)
#
#     audio_client_socket, addr = audio_server.accept()
#     print(f"Accepted audio connection from {addr}")
#     audio_clients.append(audio_client_socket)
#
#     if len(video_clients) > 1:
#         video_client_socket.sendall("start".encode())
#
#     threading.Thread(target=handle_client_video).start()
#     threading.Thread(target=handle_client_audio, args=(audio_client_socket,)).start()
