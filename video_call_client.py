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


# function to record video and send it
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


# function to receive frames and show them
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


# function to record audio and send it
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


server_ip = "192.168.1.101"

video_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_client_socket.connect((server_ip, 12345))

audio_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_client_socket.connect((server_ip, 12346))

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
