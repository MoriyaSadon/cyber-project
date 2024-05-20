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

client2_ip = "0.0.0.0"

video_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_client_socket.connect(("127.0.0.1", 12345))

audio_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_client_socket.connect(("127.0.0.1", 12346))

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
# import cv2
# import numpy as np
# from PIL import Image, ImageTk
# import tkinter as tk
#
# # Function to receive video frames from the server
# def receive_video_frames(video_client):
#     try:
#         while True:
#             size = struct.unpack('!I', video_client.recv(4))[0]
#             data = b""
#             while len(data) < size:
#                 packet = video_client.recv(size - len(data))
#                 if not packet:
#                     break
#                 data += packet
#
#             frame_data = np.frombuffer(data, dtype=np.uint8)
#             frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
#
#             # Display the frame in the GUI
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(frame)
#             img = ImageTk.PhotoImage(image=img)
#             panel.img = img
#             panel.config(image=img)
#
#     except Exception as e:
#         print(f"Error receiving video frames: {e}")
#         root.destroy()
#
# # Connect to the server for video
# video_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# video_client.connect(("192.168.1.101", 12345))
#
# # Function to handle video frames in the GUI
# def update_video():
#     threading.Thread(target=receive_video_frames, args=(video_client,), daemon=True).start()
#
# # GUI setup using Tkinter
# root = tk.Tk()
# root.title("Video Chat Client")
#
# # Create a label for displaying video frames
# panel = tk.Label(root)
# panel.pack(padx=10, pady=10)
#
# # Start receiving and displaying video frames
# update_video()
#
# # Start the Tkinter main loop
# root.mainloop()





