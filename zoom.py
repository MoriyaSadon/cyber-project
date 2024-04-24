# Client

import socket
import threading
import struct
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import sounddevice as sd
import numpy as np

# Set up client sockets for video and audio
video_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_client.connect(("127.0.0.1", 12345))

audio_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_client.connect(("127.0.0.1", 12346))


# Function to handle a single client's video stream
def handle_client_video():
    connection = video_client.makefile('wb')
    try:
        cap = cv2.VideoCapture(0)  # 0 for the default camera
        # Set the resolution of the captured frames
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            ret, frame = cap.read()

            # Resize frame to reduce data size
            resized_frame = cv2.resize(frame, (320, 240))

             # Compress and serialize the frame
            encoded_frame = cv2.imencode('.jpg', resized_frame)[1]
            serialized_frame = pickle.dumps(encoded_frame)

            # Send the size of the serialized frame
            size = len(serialized_frame)
            size_data = struct.pack('!I', size)
            video_client.sendall(size_data)

            # Send the serialized frame
            video_client.sendall(serialized_frame)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        connection.close()
        video_client.close()


# Function to update video frames in the GUI
def update_video():
    try:
        while True:
            # Receive the size of the incoming frame
            size = struct.unpack('!I', video_client.recv(4))[0]
            print(size)
            # Receive and deserialize the frame
            data = b""
            while len(data) < size:
                packet = video_client.recv(size - len(data))
                if not packet:
                    break
                data += packet

            if not data:
                break

            frame = pickle.loads(data)

            # Update the video panel
            frame = cv2.cvtColor(np.float32(frame), cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            panel.img = img
            panel.config(image=img)
            panel.image = img

    except Exception as e:
        print(f"Error: {e}")
        root.destroy()


# Function to handle a single client's audio stream
def handle_client_audio():
    connection = audio_client.makefile('wb')
    try:
        while True:
            # Record audio from microphone
            data = sd.rec(44100, channels=2, dtype=np.int16)
            sd.wait()

            # Serialize the audio data and send it to the server
            data_serialized = pickle.dumps(data)
            size = struct.pack('!I', len(data_serialized))
            audio_client.sendall(size)
            audio_client.sendall(data_serialized)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()
        audio_client.close()

# Function to play received audio
def play_audio():
    try:
        while True:
            # Receive the size of the incoming audio data
            size = struct.unpack('!I', audio_client.recv(4))[0]
            # Receive and deserialize the audio data
            data = b""
            while len(data) < size:
                packet = audio_client.recv(size - len(data))
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

msg = video_client.recv(1024).decode()
if msg == "start":
    # Start new threads to handle video reception and audio playback
    threading.Thread(target=handle_client_video, daemon=True).start()
    threading.Thread(target=update_video, daemon=True).start()
    threading.Thread(target=handle_client_audio, daemon=True).start()
    threading.Thread(target=play_audio, daemon=True).start()


# Start the Tkinter main loop
root.mainloop()



























# from vidstream import *
# import tkinter as tk
# import socket
# import threading
#
# local_ip_address = socket.gethostbyname(socket.gethostname())
#
# server = StreamingServer(local_ip_address, 9999)
# receiver = AudioReceiver(local_ip_address, 8888)
#
# def start_listening():
#     t1 = threading.Thread(target=server.start_server)
#     t2 = threading.Thread(target=receiver.start_server)
#     t1.start()
#     t2.start()
#
# def start_camera_stream():
#     camera_client = CameraClient(text_target_ip.get(1.0, 'end-1c'), 7777)
#     t3 = threading.Thread(target=camera_client.start_stream)
#     t3.start()
#
# def start_screen_sharing():
#     screen_client = ScreenShareClient(text_target_ip.get(1.0, 'end-1c'), 7777)
#     t3 = threading.Thread(target=screen_client.start_stream)
#     t3.start()
#
# def start_audio_stream():
#     audio_sender = AudioSender(text_target_ip.get(1.0, 'end-1c'), 6666)
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

