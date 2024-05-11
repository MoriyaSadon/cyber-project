import socket
import threading
from tkinter import messagebox
from gui_class import Gui1
import Encryptions_class

# Client configuration
HOST = '127.0.0.1'
PORT = 7000

private_key, public_key = Encryptions_class.generate_key_pair()

admin_help_msg = """** Hi there!
    Here are the functions you can use:
        1. video call
        2. get all the usernames in the chat - use button "users in chat"
        3. chat with friends
        4. private chat with a member - enter 'dm <name>:<message>'
        
    Also, because you're an admin you have more options:
        1. mute someone - use button "mute" -> "specific user"   
        2. mute all non admin users - use button "mute" -> "everyone" 
        3. unmute someone - use button "unmute" -> "specific user" 
        4. unmute everyone - use button "unmute" -> "everyone" 
        5. kick a user - use button "kick"
        6. add/remove censored word - use button "edit censored words" -> "add"/"remove"
        7. make a user an admin - use button "make admin"
    To return to this message click "help" button
    Have fun!! **"""
help_msg = """** Hi there!
    Here are the functions you can use:
        1. video call
        2. get all the usernames in the chat - use button "users in chat"
        3. chat with friends
        4. private chat with a member - enter 'dm <name>:<message>'
    To return to this message click "help" button
    Have fun!! **"""

# messages protocol
CHAT = "1"
FUNCS = "2"
MSGBOX = "3"
LARGE_CHAT = "14"
LARGE_MSGBOX = "34"

# encrypts a message with RSA
def encrypt_message(message):
    enc_message = Encryptions_class.encrypt_message(message, server_public_key)
    return enc_message

# decrypts a RSA encoded message
def decrypt_message(enc_message):
    message = Encryptions_class.decrypt_message(enc_message, private_key)
    return message

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            enc_comm = client_socket.recv(1024)
            comm = decrypt_message(enc_comm)

            enc_message = client_socket.recv(1024)
            message = decrypt_message(enc_message)

            print(comm)
            print(message)

            if comm == MSGBOX:
                # if message == "admin_help_msg":
                #     messagebox.showinfo(title="guide", message=admin_help_msg)
                #
                # elif message == "help_msg":
                #     messagebox.showinfo(title="guide", message=help_msg)

                if message.startswith("get all usernames"):
                    messagebox.showinfo(title="users in chat", message=message[17:])

                elif message == "you are now an admin":
                    gui_obj.admin_mode = True
                    messagebox.showinfo(title="admin", message=message)
                    gui_obj.admin_buttons()

                elif "The message couldn't sent" in message:
                    messagebox.showwarning("couldn't sent", message)

                elif message == "you've been kicked...bye":
                    client_socket.close()
                else:
                    messagebox.showwarning("bad word", message)
            else:
                gui_obj.display_message(message)
        except Exception as e:
            print(e)
            print("Error receiving message")
            break

# shows the client the help msg
def help_guide():
    if admin:
        messagebox.showinfo(title="guide", message=admin_help_msg)
    else:
        messagebox.showinfo(title="guide", message=help_msg)

# send a message to the server for the chat
def send_chat_message(message):
    enc_comm = encrypt_message(CHAT)
    client_socket.send(enc_comm)

    enc_message = encrypt_message(message)
    client_socket.send(enc_message)

# sends a message to the server to use one to the tools offered
def send_funcs_message(message):
    enc_comm = encrypt_message(FUNCS)
    client_socket.send(enc_comm)

    enc_message = encrypt_message(message)
    client_socket.send(enc_message)

# sends a message to the server for a private message to a specific client
def send_priv_msg(username, message):
    enc_comm = encrypt_message(FUNCS)
    client_socket.send(enc_comm)

    msg = f"dm {username}:{message}"
    enc_message = encrypt_message(msg)
    client_socket.send(enc_message)

# log in to the chat
def log_in(username, password):
    client_socket.send(encrypt_message("Sign in"))
    if " " not in username and " " not in password:
        info_msg = f"{username} {password}"
        client_socket.send(encrypt_message(info_msg))
        enc_message = client_socket.recv(1024)
        message = decrypt_message(enc_message)
        messagebox.showinfo(title="message", message=message)
        if message == "log in succeed":
            gui_obj.chat_window()

            # Start a thread to receive messages for chat
            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()
        else:
            gui_obj.open_signin_signup_window("Sign in")
    else:
        messagebox.showinfo(title="try again", message="the username and the password can't contain a space")

# sign up to the system and get in the chat
def sign_up(username, password):
    client_socket.send(encrypt_message("Sign up"))
    if " " not in username and " " not in password:
        info_msg = f"{username} {password}"
        client_socket.send(encrypt_message(info_msg))
        enc_message = client_socket.recv(1024)
        message = encrypt_message(enc_message)
        messagebox.showinfo(title="message", message=message)
        if message == "Sign up succeed":
            gui_obj.chat_window()

            help_guide()
            # help_msg = client_socket.recv(1024).decode()
            # messagebox.showinfo(title="guide", message=help_msg)

            # Start a thread to receive messages for chat
            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()
        else:
            gui_obj.open_signin_signup_window("Sign up")
    else:
        messagebox.showinfo(title="try again", message="the username and the password can't contain a space")


# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# Receive server's public key
serialized_public_key = client_socket.recv(4096)
server_public_key = Encryptions_class.deserialize_pub_key(serialized_public_key)

# Send public key to server
serialized_public_key = Encryptions_class.serialize_pub_key(public_key)
client_socket.send(serialized_public_key)

# is admin
enc_admin = client_socket.recv(4096)
admin = decrypt_message(enc_admin)


if admin == "True":
    admin = True
else:
    admin = False

# set up GUI
gui_obj = Gui1(admin, log_in, sign_up, send_chat_message, send_funcs_message, help_guide, send_priv_msg)
gui_obj.signin_and_signup_buttons()

gui_obj.root.mainloop()


