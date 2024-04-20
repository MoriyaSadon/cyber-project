# client

import socket
# from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


# Generate RSA key pair for client
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


# Encrypt message using server's public key
def encrypt_message(message, public_key):
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

# Decrypt message using client's private key
def decrypt_message(encrypted_message, private_key):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()


# Main function
if __name__ == "__main__":
    private_key, public_key = generate_key_pair()

    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Receive server's public key
    serialized_public_key = client_socket.recv(4096)
    server_public_key = serialization.load_pem_public_key(
        serialized_public_key,
        backend=default_backend()
    )

    while True:
        message = input("Enter message: ")
        encrypted_message = encrypt_message(message, server_public_key)
        client_socket.sendall(encrypted_message)


# working client

# import socket
# import threading
#
# # Client configuration
# HOST = '127.0.0.1'
# PORT = 7000
#
#
# # Function to receive messages from the server
# def receive_messages(client_socket):
#     while True:
#         try:
#             message = client_socket.recv(1024).decode()
#             print(message)
#             if message == "you've been kicked...bye":
#                 client_socket.close()
#         except:
#             print("Error receiving message")
#             break
#
#
# # Client setup
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))
#
# # Start a thread to receive messages
# receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
# receive_thread.start()
#
# # Main loop to send messages to the server
# while True:
#     message = input()
#     client_socket.send(message.encode())
