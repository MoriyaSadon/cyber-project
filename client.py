import socket
import threading
from tkinter import messagebox
from gui_class import Gui1
from Encryptions_class import RsaEnc


# encrypts a message with RSA
def encrypt_message(message):
    enc_message = client_rsa_obj.encrypt_message(message)
    return enc_message


# decrypts a RSA encoded message
def decrypt_message(enc_message):
    message = client_rsa_obj.decrypt_message(enc_message)
    return message


# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            enc_data = client_socket.recv(1024)
        except Exception as e:
            print(e)
            print("Error receiving message")
            break
        data = decrypt_message(enc_data)

        comm = data[0]
        message = data[1:]

        if comm == MSGBOX:
            if message.startswith("get all usernames"):
                messagebox.showinfo(title="users in chat", message=message[17:])

            elif message == "you are now an admin":
                gui_obj.admin_mode = True
                messagebox.showinfo(title="admin", message=message)
                gui_obj.admin_buttons()

            elif "The message couldn't sent" in message:
                messagebox.showwarning("couldn't sent", message)

            elif message == "you've been kicked...bye":
                messagebox.showinfo(title="admin", message=message)
                client_socket.close()
            else:
                messagebox.showwarning("bad word", message)
        else:
            gui_obj.display_message(message)


# shows the client the help msg
def help_guide():
    if gui_obj.admin_mode:
        messagebox.showinfo(title="guide", message=admin_help_msg)
    else:
        messagebox.showinfo(title="guide", message=help_msg)


# send a message to the server for the chat
def send_chat_message(message):
    data = f"{CHAT}{message}"

    enc_data = encrypt_message(data)
    client_socket.send(enc_data)


# sends a message to the server to use one to the tools offered
def send_funcs_message(message):
    data = f"{FUNCS}{message}"

    enc_data = encrypt_message(data)
    client_socket.send(enc_data)


# sends a message to the server for a private message to a specific client
def send_priv_msg(username, message):
    data = f"{FUNCS}dm {username}:{message}"

    enc_data = encrypt_message(data)
    client_socket.send(enc_data)


# log in to the chat
def log_in(username, password):
    if " " not in username and " " not in password:
        info_msg = f"Signin{username} {password}"

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
    if " " not in username and " " not in password:
        info_msg = f"Signup{username} {password}"
        client_socket.send(encrypt_message(info_msg))
        enc_message = client_socket.recv(1024)
        message = decrypt_message(enc_message)
        messagebox.showinfo(title="message", message=message)
        if message == "Sign up succeed":
            gui_obj.chat_window()

            help_guide()

            # Start a thread to receive messages for chat
            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()
        else:
            gui_obj.open_signin_signup_window("Sign up")
    else:
        messagebox.showinfo(title="try again", message="the username and the password can't contain a space")


# Client configuration
HOST = '127.0.0.1'
PORT = 7000

client_rsa_obj = RsaEnc("", "")
client_rsa_obj.generate_key_pair()

admin_help_msg = """** Hi there!
    Here are the functions you can use:
        1. video call
        2. get all the usernames in the chat - use button "users in chat"
        3. chat with friends
        4. private chat with a member - use button "send private msg"
        
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
        4. private chat with a member - use button "send private msg"
    To return to this message click "help" button
    Have fun!! **"""

# messages protocol
CHAT = "1"
FUNCS = "2"
MSGBOX = "3"

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

serialized_public_key = client_rsa_obj.serialize_pub_key()

# Receive server's public key
serialized_spublic_key = client_socket.recv(4096)
server_public_key = client_rsa_obj.deserialize_pub_key(serialized_spublic_key)

# Send public key to server
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
