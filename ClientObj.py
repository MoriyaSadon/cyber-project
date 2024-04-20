import tkinter as tk

class Client:
    def __init__(self, client_socket, name, admin, mute, in_priv_chat, priv_chat_w, rsa_pub_key):
        self.client_socket = client_socket
        self.name = name
        self.admin = admin  # t/f
        self.mute = mute  # t/f
        self.in_priv_chat = in_priv_chat  # t/f
        self.priv_chat_w = priv_chat_w

        self.rsa_pub_key = rsa_pub_key










