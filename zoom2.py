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


def handle_client_video():
    # connection = client.makefile('wb')
    while True:
        # Receive the size of the incoming frame
        size = struct.unpack('!I', video_client_socket.recv(4))[0]

        # Receive and deserialize the frame
        data = b""
        while len(data) < size:
            # Determine the amount of data remaining to be received
            remaining_bytes = size - len(data)
            # Receive data in smaller chunks to avoid overflow error
            chunk = video_client_socket.recv(min(remaining_bytes, 4096))  # Adjust chunk size as needed
            if not chunk:
                # Handle case where connection is closed unexpectedly
                print("Connection closed unexpectedly")
                break
            data += chunk
            if not data:
                break

        for client in video_clients:
            if len(video_clients) > 1 and client != video_client_socket:
                data = pickle.dumps(data)
                size = struct.pack('!I', len(data))
                video_client_socket.sendall(size)
                video_client_socket.sendall(data)
                # connection.write(size)
                # connection.write(data)


# Function to handle client's audio stream
def handle_client_audio(audio_client_socket):
    try:
        while True:
            # Receive the size of the incoming audio data
            size_data = audio_client_socket.recv(4)
            if not size_data:
                break

            size = struct.unpack('!I', size_data)[0]

            # Receive and deserialize the audio data
            data = b""
            while len(data) < size:
                packet = audio_client_socket.recv(size - len(data))
                if not packet:
                    break
                data += packet

            if not data:
                break

            # Broadcast the audio data to other clients
            for client_socket in audio_clients[:]:  # Iterate over a copy of the list
                if client_socket != audio_client_socket and isinstance(client_socket, socket.socket):
                    try:
                        client_socket.send("audio".encode())
                        client_socket.sendall(struct.pack('!I', size))
                        client_socket.sendall(pickle.loads(data))

                    except Exception as e:
                        print(f"Error broadcasting audio to client: {e}")
                        # If an error occurs, assume the client has disconnected and remove it from the list
                        audio_clients.remove(client_socket)

    except Exception as e:
        print(f"Error handling audio client: {e}")
    finally:
        audio_client_socket.close()
        # Remove the client's socket from the list after closing the connection
        if audio_client_socket in audio_clients:
            audio_clients.remove(audio_client_socket)


# Set up server sockets for video and audio
video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_server.bind(("0.0.0.0", 12345))
video_server.listen()

audio_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_server.bind(("0.0.0.0", 12346))
audio_server.listen()

# Main server loop for video
while True:
    video_client_socket, addr = video_server.accept()
    print(f"Accepted video connection from {addr}")
    video_clients.append(video_client_socket)

    audio_client_socket, addr = audio_server.accept()
    print(f"Accepted audio connection from {addr}")
    audio_clients.append(audio_client_socket)

    if len(video_clients) > 1:
        video_client_socket.sendall("start".encode())

    threading.Thread(target=handle_client_video).start()
    threading.Thread(target=handle_client_audio, args=(audio_client_socket,)).start()



























# from vidstream import *
# import tkinter as tk
# import socket
# import threading
#
# local_ip_address = socket.gethostbyname(socket.gethostname())
#
# server = StreamingServer(local_ip_address, 7777)
# receiver = AudioReceiver(local_ip_address, 6666)
#
# def start_listening():
#     t1 = threading.Thread(target=server.start_server)
#     t2 = threading.Thread(target=receiver.start_server)
#     t1.start()
#     t2.start()
#
# def start_camera_stream():
#     camera_client = CameraClient(text_target_ip.get(1.0, 'end-1c'), 9999)
#     t3 = threading.Thread(target=camera_client.start_stream)
#     t3.start()
#
# def start_screen_sharing():
#     screen_client = ScreenShareClient(text_target_ip.get(1.0, 'end-1c'), 9999)
#     t5 = threading.Thread(target=screen_client.start_stream)
#     t5.start()
#
# def start_audio_stream():
#     audio_sender = AudioSender(text_target_ip.get(1.0, 'end-1c'), 8888)
#     t4 = threading.Thread(target=audio_sender.start_stream)
#     t4.start()
#
# # GUI
# window = tk.Tk()
# window.title("video call")
# window.geometry('300x200')
#
# label_target_ip = tk.Label(window, text="target ip:")
# label_target_ip.pack()
#
# text_target_ip = tk.Text(window, height=1)
# text_target_ip.pack()
#
# btn_listen = tk.Button(window, text="start listening", width=50, command=start_listening)
# btn_listen.pack(anchor=tk.CENTER, expand=True)
#
# btn_camera = tk.Button(window, text="start camera stream", width=50, command=start_camera_stream)
# btn_camera.pack(anchor=tk.CENTER, expand=True)
#
# btn_screen = tk.Button(window, text="start screen sharing", width=50, command=start_screen_sharing)
# btn_screen.pack(anchor=tk.CENTER, expand=True)
#
# btn_audio = tk.Button(window, text="start audio stream", width=50, command=start_audio_stream)
# btn_audio.pack(anchor=tk.CENTER, expand=True)
#
# window.mainloop()

