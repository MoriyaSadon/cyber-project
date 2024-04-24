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

# Function to update video frames in the GUI
def update_video():
    try:
        while True:
            # Receive the size of the incoming frame
            size = struct.unpack('!I', video_client.recv(4))[0]

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
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            panel.img = img
            panel.config(image=img)
            panel.image = img

    except Exception as e:
        print(f"Error: {e}")
        root.destroy()

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

# Start new threads to handle video reception and audio playback
threading.Thread(target=update_video, daemon=True).start()
threading.Thread(target=play_audio, daemon=True).start()

# Start the Tkinter main loop
root.mainloop()


# import socket
#
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address = ("127.0.0.1", 8200)
#
# sock.sendto('moriya'.encode(), server_address)
# data = sock.recv(1024).decode()
#
#
# sock.close()


# import cv2
# import numpy as np
# import socket
# import threading
# import time
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("127.0.0.1", 12345))
#
# cap = cv2.VideoCapture(0)  # 0 for the default camera
#
# time.sleep(1)
# def send_frames():
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Error with stream")
#             break
#
#         frame = cv2.resize(frame, (640, 480))  # Resize the frame to a standard size
#         # Uncomment the line below if you want to display the frame locally
#         # cv2.imshow('frame', frame)
#
#         encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
#         print("Sent")
#         client.send(encoded_frame)
#         time.sleep(0.1)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#
# send_thread = threading.Thread(target=send_frames)
# send_thread.start()
