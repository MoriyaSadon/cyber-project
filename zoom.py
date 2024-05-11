# Client

import socket
import threading
import struct
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

# Function to receive video frames from the server
def receive_video_frames(video_client):
    try:
        while True:
            size = struct.unpack('!I', video_client.recv(4))[0]
            data = b""
            while len(data) < size:
                packet = video_client.recv(size - len(data))
                if not packet:
                    break
                data += packet

            frame_data = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

            # Display the frame in the GUI
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            panel.img = img
            panel.config(image=img)

    except Exception as e:
        print(f"Error receiving video frames: {e}")
        root.destroy()

# Connect to the server for video
video_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_client.connect(("192.168.1.101", 12345))

# Function to handle video frames in the GUI
def update_video():
    threading.Thread(target=receive_video_frames, args=(video_client,), daemon=True).start()

# GUI setup using Tkinter
root = tk.Tk()
root.title("Video Chat Client")

# Create a label for displaying video frames
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# Start receiving and displaying video frames
update_video()

# Start the Tkinter main loop
root.mainloop()





# import socket
# import threading
# import struct
# import pickle
# import tkinter as tk
# from PIL import Image, ImageTk
# import cv2
# import sounddevice as sd
# import numpy as np
#
# # Set up client sockets for video and audio
# video_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# video_client.connect(("127.0.0.1", 12345))
#
# audio_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# audio_client.connect(("127.0.0.1", 12346))
#
#
# # Function to handle a single client's video stream
# def handle_client_video():
#     connection = video_client.makefile('wb')
#     try:
#         cap = cv2.VideoCapture(0)  # 0 for the default camera
#         # Set the resolution of the captured frames
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
#         while True:
#             ret, frame = cap.read()
#
#             # Resize frame to reduce data size
#             resized_frame = cv2.resize(frame, (320, 240))
#
#              # Compress and serialize the frame
#             encoded_frame = cv2.imencode('.jpg', resized_frame)[1]
#             serialized_frame = pickle.dumps(encoded_frame)
#
#             # Send the size of the serialized frame
#             size = len(serialized_frame)
#             size_data = struct.pack('!I', size)
#             video_client.sendall(size_data)
#
#             # Send the serialized frame
#             video_client.sendall(serialized_frame)
#
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         cap.release()
#         connection.close()
#         video_client.close()
#
#
# # Function to update video frames in the GUI
# def update_video():
#     try:
#         while True:
#             # Receive the size of the incoming frame
#             size = struct.unpack('!I', video_client.recv(4))[0]
#             print(size)
#             # Receive and deserialize the frame
#             data = b""
#             while len(data) < size:
#                 packet = video_client.recv(size - len(data))
#                 if not packet:
#                     break
#                 data += packet
#
#             if not data:
#                 break
#
#             frame = pickle.loads(data)
#
#             # Update the video panel
#             frame = cv2.cvtColor(np.float32(frame), cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(frame)
#             img = ImageTk.PhotoImage(img)
#             panel.img = img
#             panel.config(image=img)
#             panel.image = img
#
#     except Exception as e:
#         print(f"Error: {e}")
#         root.destroy()
#
#
# # Function to handle a single client's audio stream
# def handle_client_audio():
#     connection = audio_client.makefile('wb')
#     try:
#         while True:
#             # Record audio from microphone
#             data = sd.rec(44100, channels=2, dtype=np.int16)
#             sd.wait()
#
#             # Serialize the audio data and send it to the server
#             data_serialized = pickle.dumps(data)
#             size = struct.pack('!I', len(data_serialized))
#             audio_client.sendall(size)
#             audio_client.sendall(data_serialized)
#
#     except Exception as e:
#         print(f"Error: {e}")
#
#     finally:
#         connection.close()
#         audio_client.close()
#
# # Function to play received audio
# def play_audio():
#     try:
#         while True:
#             # Receive the size of the incoming audio data
#             size = struct.unpack('!I', audio_client.recv(4))[0]
#             # Receive and deserialize the audio data
#             data = b""
#             while len(data) < size:
#                 packet = audio_client.recv(size - len(data))
#                 if not packet:
#                     break
#                 data += packet
#
#             if not data:
#                 break
#
#             # Play the audio
#             audio_data = pickle.loads(data)
#             sd.play(audio_data, samplerate=44100, blocking=False)
#
#     except Exception as e:
#         print(f"Error: {e}")
#         root.destroy()
#
#
# # GUI setup using Tkinter
# root = tk.Tk()
# root.title("Video Chat Client")
#
# # Create a label for displaying video frames
# panel = tk.Label(root)
# panel.pack(padx=10, pady=10)
#
# msg = video_client.recv(1024).decode()
# if msg == "start":
#     # Start new threads to handle video reception and audio playback
#     threading.Thread(target=handle_client_video, daemon=True).start()
#     threading.Thread(target=update_video, daemon=True).start()
#     threading.Thread(target=handle_client_audio, daemon=True).start()
#     threading.Thread(target=play_audio, daemon=True).start()
#
#
# # Start the Tkinter main loop
# root.mainloop()
