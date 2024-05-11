import socket
import threading
from ClientObj import Client
from firebase_class import Firebase
from hashlib import sha256
import Encryptions_class

# Server configuration
HOST = '127.0.0.1'
PORT = 7000

# List to store connected clients
clients = []

admin_help_msg = """** Hi there!
    Here are the functions you can use:
        1. video call
        2. get all the usernames in the chat - enter 'get all usernames'
        3. chat with friends
        4. private chat with a member - enter 'dm <name>:<message>'
        
    Also, because you're an admin you have more options:
        1. mute someone - enter mute:<name>
        2. unmute someone - enter 'unmute:<name>'
        3. mute all non admin users - enter 'mute everyone'
        4. kick a user - enter 'kick:<name>'
        5. add/remove censored word - enter '<add/remove>:<word>'
    to return to this message enter 'help'
    have fun!! **"""
help_msg = """** Hi there!
    Here are the functions you can use:
        1. video call
        2. get all the usernames in the chat - enter 'get all usernames'
        3. chat with friends
        4. private chat with a member - enter 'dm <name>:<message>'
    to return to this message enter 'help'
    have fun!! **"""

users_firebase = Firebase("Users")
censored_firebase = Firebase("Censored")


def send_encrypted_msg(my_client: Client, msg):
    pub_key = my_client.rsa_pub_key
    encrypted_msg = Encryptions_class.encrypt_message(msg, pub_key)
    my_client.client_socket.send(encrypted_msg)


def check_username(my_client: Client, username):
    while True:
        hashed_username = sha256(username.encode()).hexdigest()
        if hashed_username in users_firebase.get_childs_lst():
            my_client.client_socket.send("this username is already used, please enter a different one".encode())
            username = my_client.client_socket.recv(1024).decode()
        else:
            # my_client.name = username
            return hashed_username


def sign_up(my_client: Client):
    my_client.client_socket.send("enter username: ".encode())
    username = my_client.client_socket.recv(1024).decode()
    hashed_username = check_username(my_client, username)

    my_client.client_socket.send("enter password: ".encode())
    password = my_client.client_socket.recv(1024).decode()
    hashed_pass = sha256(password.encode()).hexdigest()

    user = Firebase(f"Users/{hashed_username}")
    user.update_value("name", hashed_username)
    user.update_value("password", hashed_pass)

    my_client.client_socket.send("sign up succeed".encode())
    my_client.name = username


def check_password(my_client: Client, username, password):
    user = Firebase(f"Users/{username}")
    for i in range(3):
        hashed_pass = sha256(password.encode()).hexdigest()
        if hashed_pass != user.get_data("password"):
            my_client.client_socket.send("wrong password... enter a different one".encode())
            password = my_client.client_socket.recv(1024).decode()
        else:
            return True
    return False


def log_in(my_client: Client):
    my_client.client_socket.send("enter username: ".encode())
    username = my_client.client_socket.recv(1024).decode()
    hashed_username = sha256(username.encode()).hexdigest()
    if hashed_username in users_firebase.get_childs_lst():
        my_client.client_socket.send("enter password: ".encode())
        password = my_client.client_socket.recv(1024).decode()

        is_in = check_password(my_client, hashed_username, password)
        if is_in:
            my_client.client_socket.send("log in succeed".encode())
            my_client.name = username
        else:
            my_client.client_socket.send("you ran out of tries...".encode())


def approve_message_content(my_client: Client, message):
    for word in censored_firebase.get_childs_lst():
        word_obj = Firebase(f"Censored/{word.lower()}")
        if word_obj.get_data("on") == "yes" and word in message.lower():
            my_client.client_socket.send(f"the word '{word}' isn't approved.".encode())
            return False
    return True


def broadcast(message, my_client: Client):
    for client in clients:
        if client != my_client and client.name:
            try:
                message = f"{my_client.name}: {message}"
                send_encrypted_msg(client, message)
            except Exception:
                # Remove the client if unable to send a message
                clients.remove(client)


def send_everyone(message):
    for client in clients:
        message = f"-- {message} --"
        client.client_socket.send(message.encode())


def get_all_usernames():
    num = 1
    names_str = ""
    for client in clients:
        names_str += f"{num}. {client.name}\n"
        num += 1
    return names_str


def priv_chat(my_client: Client, message):
    name = message.split(":")[0][2:].strip()
    print(name)
    msg = message.split(":")[1]
    check = False
    for client in clients:
        if client.name == name:
            client.client_socket.send(f"--> {my_client.name}: {msg}".encode())
            check = True
    if not check:
        my_client.client_socket.send("The username doesnt exist...".encode())


# admin only
def mute_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.mute = True
    send_everyone(f"{user_name} has been muted")


def unmute_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.mute = False
    send_everyone(f"{user_name} has been unmuted")


def mute_not_admins():
    for client in clients:
        if not client.admin:
            client.mute = True
    send_everyone("-- only admins can send msgs --")


def kick_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.client_socket.send("you've been kicked...bye".encode())
            client_thread.join()
            client.client_socket.close()
    send_everyone(f"{user_name} has been kicked")


def add_censored_word(word):
    censored_word = Firebase(f"Censored/{word.lower()}")
    censored_word.update_value("on", "yes")


def approve_censored_word(word):
    word1 = Firebase(f"Censored/{word.lower()}")
    word1.update_value("on", "no")


# Function to handle incoming messages from a client
def handle_client(current_client: Client):
    # current_client.client_socket.send("sign up/log in ?".encode())
    # comm = current_client.client_socket.recv(1024).decode()
    # if comm.lower() == "sign up":
    #     sign_up(current_client)
    #     if current_client.admin:
    #         current_client.client_socket.send(admin_help_msg.encode())
    #     else:
    #         current_client.client_socket.send(help_msg.encode())
    # else:
    #     log_in(current_client)

    send_encrypted_msg(current_client, "please enter your name")
    encrypted_msg = current_client.client_socket.recv(1024)
    name = Encryptions_class.decrypt_message(encrypted_msg, private_key)
    current_client.name = name
    while True:
        try:
            encrypted_msg = current_client.client_socket.recv(1024)
            message = Encryptions_class.decrypt_message(encrypted_msg, private_key)
            print(message)
            if not message:
                break

            if message.lower() == "help":
                if current_client.admin:
                    current_client.client_socket.send(admin_help_msg.encode())
                else:
                    current_client.client_socket.send(help_msg.encode())

            elif "unmute" in message.lower():
                if current_client.admin:
                    user_name = message.split(":")[1]  # unmute:name
                    unmute_user(user_name)
                else:
                    current_client.client_socket.send("** You're not an admin, therefore you cant do that **".encode())

            elif "mute everyone" in message.lower():
                mute_not_admins()

            elif "mute" in message.lower():
                if current_client.admin:
                    user_name = message.split(":")[1]  # mute:name
                    mute_user(user_name)
                else:
                    current_client.client_socket.send("** You're not an admin, therefore you cant do that **".encode())

            elif "kick" in message.lower():
                if current_client.admin:
                    username = message.split(":")[1]  # kick:name
                    kick_user(username)
                else:
                    current_client.client_socket.send("** You're not an admin, therefore you cant do that **".encode())

            elif "add censored word" in message.lower():
                if current_client.admin:
                    word = message.split(":")[1]  # add censored word:word
                    add_censored_word(word)
                else:
                    current_client.client_socket.send("** You're not an admin, therefore you cant do that **".encode())

            elif "approve censored word" in message.lower():
                if current_client.admin:
                    word = message.split(":")[1]  # approve censored word:word
                    approve_censored_word(word)
                else:
                    current_client.client_socket.send("** You're not an admin, therefore you cant do that **".encode())

            elif message.lower() == "get all usernames":
                current_client.client_socket.send(get_all_usernames().encode())

            elif message.lower().startswith("dm "):
                priv_chat(current_client, message)  # dm name:msg

            else:
                if not current_client.mute and approve_message_content(current_client, message):
                    broadcast(message, current_client)
                else:
                    current_client.client_socket.send("The message couldn't sent".encode())
        except Exception:
            # Remove the client if an error occurs
            clients.remove(current_client)
            break


# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# Accept and handle incoming connections
while True:
    if len(clients) >= 1:
        admin = False
    else:
        admin = True

    client_socket, addr = server_socket.accept()
    current_client = Client(client_socket, "", admin, False, "")
    clients.append(current_client)

    private_key, public_key = Encryptions_class.generate_key_pair()

    # Receive client's public key
    serialized_client_pub_key = client_socket.recv(4096)
    client_pub_key = Encryptions_class.deserialize_pub_key(serialized_client_pub_key)
    current_client.rsa_pub_key = client_pub_key

    # Send public key to client
    serialized_public_key = Encryptions_class.serialize_pub_key(public_key)
    client_socket.send(serialized_public_key)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(current_client,))
    client_thread.start()
