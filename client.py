import socket
import threading
import tkinter as tk
from tkinter import messagebox
from gui_class import Gui1
from hashlib import sha256

# Client configuration
HOST = '127.0.0.1'
PORT = 7000


# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if "$get all usernames$" in message:
                get_users_lst(message)
            elif "The message couldn't sent" in message:
                messagebox.showwarning("couldn't sent", message)
            elif message.startswith("cw##"):
                messagebox.showwarning("bad word", message[4:])
            elif message == "you've been kicked...bye":
                client_socket.close()
            else:
                gui_obj.display_message(message)
        except:
            print("Error receiving message")
            break

def send_message(message):
    client_socket.send(message.encode())


def log_in(username, password):
    client_socket.send("Sign in".encode())
    if " " not in username and " " not in password:
        client_socket.send(f"{username} {password}".encode())
        message = client_socket.recv(1024).decode()
        messagebox.showinfo(title="message", message=message)
        if message == "log in succeed":
            message = client_socket.recv(1024).decode()
            admin = message.split(":")[1]
            gui_obj.chat_window(admin)

            # Start a thread to receive messages for chat
            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()
        else:
            gui_obj.open_signin_signup_window("Sign in")
    else:
        messagebox.showinfo(title="try again", message="the username and the password can't contain a space")

def sign_up(username, password):
    client_socket.send("Sign up".encode())
    if " " not in username and " " not in password:
        client_socket.send(f"{username} {password}".encode())
        message = client_socket.recv(1024).decode()
        messagebox.showinfo(title="message", message=message)
        if message == "Sign up succeed":
            message = client_socket.recv(1024).decode()
            admin = message.split(":")[1]
            gui_obj.chat_window(admin)

            help_msg = client_socket.recv(1024).decode()
            messagebox.showinfo(title="guide", message=help_msg)

            # Start a thread to receive messages for chat
            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()
        else:
            gui_obj.open_signin_signup_window("Sign up")
    else:
        messagebox.showinfo(title="try again", message="the username and the password can't contain a space")


def get_users_lst(message):
    lst = message.split("$")[2]
    messagebox.showinfo(title="users in chat", message=lst)


# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

gui_obj = Gui1(log_in, sign_up, send_message)
gui_obj.signin_and_signup_buttons()

gui_obj.root.mainloop()


