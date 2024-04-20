import cv2
import socket
import struct
import pickle
import threading

# Server
class VideoChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")

            self.connections.append(client_socket)

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        try:
            while True:
                data = b""
                payload_size = struct.calcsize(">L")

                while len(data) < payload_size:
                    data += client_socket.recv(4096)

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4096)

                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                print(frame)
                # print(type(cv2.imdecode(frame,1)))
                # frame = cv2.imdecode(frame, 1)

                cv2.imshow('Video from client', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except (socket.error, struct.error, pickle.UnpicklingError):
            print("Connection closed.")
            self.connections.remove(client_socket)
            client_socket.close()

# Client
class VideoChatClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.server_address, self.server_port))
        print(f"Connected to server at {self.server_address}:{self.server_port}")

    def send_video(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            data = pickle.dumps(frame)
            size = len(data)

            try:
                self.client_socket.sendall(struct.pack(">L", size) + data)
            except socket.error:
                print("Server disconnected.")
                break

        cap.release()
        self.client_socket.close()


if __name__ == '__main__':
    # Start the server in a separate thread
    server = VideoChatServer('127.0.0.1', 8080)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    # Create a client and connect to the server
    client = VideoChatClient('127.0.0.1', 8080)
    client.connect()

    # Start sending video from the client
    client_thread = threading.Thread(target=client.send_video)
    client_thread.start()

    # Keep the program running
    server_thread.join()
    client_thread.join()


# import cv2
#
# def video_call():
#     # Open a connection to the webcam (0 represents the default camera)
#     cap = cv2.VideoCapture(0)
#
#     # Check if the camera is opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return
#
#     while True:
#         # Read a frame from the camera
#         ret, frame = cap.read()
#
#         # Display the frame in a window
#         cv2.imshow('Video Call', frame)
#
#         # Break the loop if 'q' key is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Release the camera and close the window
#     cap.release()
#     cv2.destroyAllWindows()
#
# if __name__ == "__main__":
#     video_call()
