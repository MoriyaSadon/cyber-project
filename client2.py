import socket
import threading
import Encryptions_class
from cryptography.hazmat.primitives import serialization

# Client configuration
HOST = '127.0.0.1'
PORT = 7000


# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            message = Encryptions_class.decrypt_message(encrypted_message, private_key)
            print(message)
            if message == "you've been kicked...bye":
                client_socket.close()
        except:
            print("Error receiving message")
            break


# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

private_key, public_key = Encryptions_class.generate_key_pair()

# Send public key to server
serialized_public_key = Encryptions_class.serialize_pub_key(public_key)
client_socket.send(serialized_public_key)

# Receive server's public key
serialized_public_key = client_socket.recv(4096)
server_public_key = Encryptions_class.deserialize_pub_key(serialized_public_key)

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Main loop to send messages to the server
while True:
    message = input()
    encrypted_msg = Encryptions_class.encrypt_message(message, server_public_key)
    client_socket.send(encrypted_msg)














































# import socket
# import threading
# import Encryptions_class
#
# # Client configuration
# HOST = '127.0.0.1'
# PORT = 7000
#
# # rsa keys
# pem_format_rsa, private_key_rsa = Encryptions_class.generate_keys_rsa()
#
#
# # Function to receive messages from the server
# def receive_messages(client_socket):
#     while True:
#         # try:
#         encoded_message = str(client_socket.recv(1024).decode())
#         print(encoded_message)
#         print("gfukgk", len(encoded_message))
#         message = Encryptions_class.decrypt_msg_rsa(encoded_message, private_key_rsa)
#         print(message)
#         if message == "you've been kicked...bye":
#             client_socket.close()
#     # except:
#     #     print("Error receiving message")
#     #     break
#
#
# # Client setup
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))
#
# # getting the server's public key
# server_pub_key_64 = client_socket.recv(1024).decode()
# server_pub_key = Encryptions_class.decrypt_pubkey_64(server_pub_key_64)  # bytes
#
# # sending the public key to server to keep in the obj
# client_socket.send(Encryptions_class.encrypt_pubkey_64(server_pub_key))
#
# # Start a thread to receive messages
# receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
# receive_thread.start()
#
# # Main loop to send messages to the server
# while True:
#     message = input()
#     encoded_message = Encryptions_class.encrypt_msg_rsa(message, server_pub_key)
#     client_socket.send(encoded_message)
