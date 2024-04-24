import socket
import threading
from ClientObj import Client
from firebase_class import Firebase
from hashlib import sha256

# Server configuration
HOST = '127.0.0.1'
PORT = 7000

# List to store connected clients
clients = []

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

users_firebase = Firebase("Users")
censored_firebase = Firebase("Censored")


def sign_up(username, password):
    hashed_username = sha256(username.encode()).hexdigest()
    print(users_firebase.get_childs_lst())
    if hashed_username not in users_firebase.get_childs_lst():
        hashed_pass = sha256(password.encode()).hexdigest()

        user = Firebase(f"Users/{hashed_username}")
        user.update_value("name", hashed_username)
        user.update_value("password", hashed_pass)

        print("yes")
        current_client.client_socket.send("Sign up succeed".encode())
        current_client.name = username
        return True
    else:
        current_client.client_socket.send("This username is already used, please enter a different one".encode())
    return False


def check_password(username, password):
    user = Firebase(f"Users/{username}")
    hashed_pass = sha256(password.encode()).hexdigest()
    if hashed_pass != user.get_data("password"):
        current_client.client_socket.send("wrong password".encode())
        return False
    else:
        return True


def log_in(username, password):
    hashed_username = sha256(username.encode()).hexdigest()
    if hashed_username in users_firebase.get_childs_lst():
        is_in = check_password(hashed_username, password)
        if is_in:
            current_client.client_socket.send("log in succeed".encode())
            current_client.name = username
            return True
    else:
        current_client.client_socket.send("wrong username".encode())
    return False


def approve_message_content(my_client: Client, message):
    for word in censored_firebase.get_childs_lst():
        word_obj = Firebase(f"Censored/{word.lower()}")
        if word_obj.get_data("on") == "yes" and word in message.lower():
            my_client.client_socket.send(f"cw##the word '{word}' isn't approved.".encode())
            return False
    return True


def broadcast(message, my_client: Client):
    for client in clients:
        if client != my_client and client.name:
            try:
                message = f"{my_client.name}: {message}"
                client.client_socket.send(message.encode())
            except Exception:
                # Remove the client if unable to send a message
                clients.remove(client)


def send_everyone(message):
    for client in clients:
        message = f"-- {message} --"
        client.client_socket.send(message.encode())


def get_all_usernames():
    num = 1
    names_str = "$get all usernames$"
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
def make_admin(username):
    for client in clients:
        if client.name == username:
            client.admin = True
            client.client_socket.send("a##you are now an admin".encode())
            send_everyone(f"{username} is now an admin")

def mute_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.mute = True
    send_everyone(f"{user_name} has been muted")

def mute_not_admins():
    for client in clients:
        if not client.admin:
            client.mute = True
    send_everyone("only admins can send msgs")

def unmute_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.mute = False
    send_everyone(f"{user_name} has been unmuted")

def unmute_everyone():
    for client in clients:
        client.mute = False
    send_everyone("everyone is unmuted")

def kick_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.client_socket.send("you've been kicked...bye".encode())
            client_thread.join()
            client.client_socket.close()
    send_everyone(f"{user_name} has been kicked")


def add_censored_word(word):
    print("in")
    censored_word = Firebase(f"Censored/{word.lower()}")
    censored_word.update_value("on", "yes")
    send_everyone(f"{current_client.name} banned the word {word} from the chat")


def approve_censored_word(word):
    word1 = Firebase(f"Censored/{word.lower()}")
    word1.update_value("on", "no")
    send_everyone(f"{current_client.name} allowed the word {word} for use in the chat")


# Function to handle incoming messages from a client
def handle_client(current_client: Client):
    check = False
    while not check:
        comm = current_client.client_socket.recv(1024).decode()
        data = current_client.client_socket.recv(1024).decode().split(" ")
        username = data[0]
        password = data[1]
        if comm.lower() == "sign up":
            check = sign_up(username, password)
            if current_client.admin:
                current_client.client_socket.send(admin_help_msg.encode())
            else:
                current_client.client_socket.send(help_msg.encode())
        else:
            check = log_in(username, password)

    while True:
        try:
            message = current_client.client_socket.recv(1024).decode()
            if not message:
                break

            if message.lower() == "help":
                if current_client.admin:
                    current_client.client_socket.send(admin_help_msg.encode())
                else:
                    current_client.client_socket.send(help_msg.encode())

            if "make admin" in message.lower():
                username = message.split(":")[1]  # make admin:name
                make_admin(username)

            elif message == "unmute everyone":
                unmute_everyone()

            elif "unmute" in message.lower():
                if current_client.admin:
                    user_name = message.split(":")[1]  # unmute:name
                    unmute_user(user_name)

            elif "mute everyone" in message.lower():
                mute_not_admins()

            elif "mute" in message.lower():
                if current_client.admin:
                    user_name = message.split(":")[1]  # mute:name
                    mute_user(user_name)

            elif "kick" in message.lower():
                if current_client.admin:
                    username = message.split(":")[1]  # kick:name
                    kick_user(username)

            elif "add censored word" in message.lower():
                if current_client.admin:
                    word = message.split(":")[1]  # add censored word:word
                    add_censored_word(word)

            elif "remove censored word" in message.lower():
                if current_client.admin:
                    word = message.split(":")[1]  # approve censored word:word
                    approve_censored_word(word)

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
    current_client = Client(client_socket, "", admin, False, False, "", "")
    clients.append(current_client)

    print(admin)

    # send if the user is an admin
    current_client.client_socket.send(str(admin).encode())

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(current_client,))
    client_thread.start()
