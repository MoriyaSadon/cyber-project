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

CHAT = "1"
FUNCS = "2"
MSGBOX = "3"
LARGE_CHAT = "14"
LARGE_MSGBOX = "34"

users_firebase = Firebase("Users")
censored_firebase = Firebase("Censored")

private_key, public_key = Encryptions_class.generate_key_pair()

# encrypts a message with RSA
def encrypt_message(my_client: Client, message):
    pub_key = my_client.rsa_pub_key
    enc_msg = Encryptions_class.encrypt_message(message, pub_key)
    return enc_msg

# decrypts a RSA encoded message
def decrypt_message(enc_message):
    message = Encryptions_class.decrypt_message(enc_message, private_key)
    return message

# sign up a user in the system
def sign_up(username, password):
    hashed_username = sha256(username.encode()).hexdigest()
    print(users_firebase.get_childs_lst())
    if hashed_username not in users_firebase.get_childs_lst():
        hashed_pass = sha256(password.encode()).hexdigest()

        user = Firebase(f"Users/{hashed_username}")
        user.update_value("name", hashed_username)
        user.update_value("password", hashed_pass)

        current_client.client_socket.send(encrypt_message(current_client, "Sign up succeed"))
        current_client.name = username
        return True
    else:
        current_client.client_socket.send(encrypt_message(current_client, "This username is already used, please enter a different one"))
    return False


# check if the password is correct for the username
def check_password(username, password):
    user = Firebase(f"Users/{username}")
    hashed_pass = sha256(password.encode()).hexdigest()
    if hashed_pass != user.get_data("password"):
        current_client.client_socket.send(encrypt_message(current_client, "wrong password"))
        return False
    else:
        return True

# log in a user to the chat
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


# check the message for bad words that are censored in the database
def approve_message_content(my_client: Client, message):
    for word in censored_firebase.get_childs_lst():
        word_obj = Firebase(f"Censored/{word.lower()}")
        if word_obj.get_data("on") == "yes" and word in message.lower():
            my_client.client_socket.send(MSGBOX.encode())
            my_client.client_socket.send(encrypt_message(current_client, f"The word '{word}' isn't approved."))
            return False
    return True


# send all the other clients a client's message
def broadcast(message, my_client: Client):
    for client in clients:
        if client != my_client and client.name:
            try:
                message = f"{my_client.name}: {message}"
                # client.client_socket.send(CHAT.encode())
                client.client_socket.send(encrypt_message(client, CHAT))
                client.client_socket.send(encrypt_message(client, message))
            except Exception:
                # Remove the client if unable to send a message
                clients.remove(client)


# send a message to all the clients in the chat
def send_everyone(message):
    for client in clients:
        message = f"-- {message} --"
        client.client_socket.send(CHAT.encode())
        client.client_socket.send(encrypt_message(client, message))


# get a list of the users connected to the chat
def get_all_usernames():
    num = 1
    names_str = "get all usernames"
    for client in clients:
        names_str += f"{num}. {client.name}\n"
        num += 1
    current_client.client_socket.send(encrypt_message(current_client, MSGBOX))
    current_client.client_socket.send(encrypt_message(current_client, names_str))


# send a private message to a specific user
def priv_chat(my_client: Client, message):
    name = message.split(":")[0][2:].strip()
    print(name)
    msg = message.split(":")[1]
    check = False
    for client in clients:
        if client.name == name:
            client.client_socket.send(CHAT.encode())
            client.client_socket.send(f"--> {my_client.name}: {msg}".encode())
            check = True
    if not check:
        my_client.client_socket.send(CHAT.encode())
        my_client.client_socket.send("** The username doesnt exist... **".encode())


# --admin only--
# make a specific user an admin in the chat
def make_admin(username):
    for client in clients:
        if client.name == username:
            client.admin = True
            client.client_socket.send(MSGBOX.encode())
            client.client_socket.send("you are now an admin".encode())
            send_everyone(f"{username} is now an admin")

# mute a specific user in the chat so that he can't send messages
def mute_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.mute = True
    send_everyone(f"{user_name} has been muted")

# mute all users in chat except for admins
def mute_not_admins():
    for client in clients:
        if not client.admin:
            client.mute = True
    send_everyone("only admins can send msgs")

# unmute a specific user so that he can send messages again
def unmute_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.mute = False
    send_everyone(f"{user_name} has been unmuted")

# unmute everyone in the chat
def unmute_everyone():
    for client in clients:
        client.mute = False
    send_everyone("everyone is unmuted")

# kick a specific user from the chat
def kick_user(user_name):
    for client in clients:
        if client.name == user_name:
            client.client_socket(MSGBOX.encode())
            client.client_socket.send("you've been kicked...bye".encode())
            client_thread.join()
            client.client_socket.close()
    send_everyone(f"{user_name} has been kicked")

# add a word to the censored words list in database
def add_censored_word(word):
    print("in")
    censored_word = Firebase(f"Censored/{word.lower()}")
    censored_word.update_value("on", "yes")
    send_everyone(f"{current_client.name} banned the word {word} from the chat")

# remove a word from the censored words list in the database
def approve_censored_word(word):
    word1 = Firebase(f"Censored/{word.lower()}")
    word1.update_value("on", "no")
    send_everyone(f"{current_client.name} allowed the word {word} for use in the chat")


# Function to handle incoming messages from a client
def handle_client(current_client: Client):
    check = False
    while not check:
        comm = current_client.client_socket.recv(1024).decode()
        # comm = decrypt_message(enc_comm)
        data = current_client.client_socket.recv(1024).decode().split(" ")
        # data = decrypt_message(enc_data).split(" ")
        username = data[0]
        password = data[1]
        if comm.lower() == "sign up":
            check = sign_up(username, password)
            current_client.client_socket.send(MSGBOX.encode())
            if current_client.admin:
                current_client.client_socket.send(encrypt_message(current_client,"admin_help_msg"))
            else:
                current_client.client_socket.send(encrypt_message(current_client, "help_msg"))
        else:
            check = log_in(username, password)

    while True:
        try:
            enc_comm = current_client.client_socket.recv(1024)
            comm = decrypt_message(enc_comm)
            enc_message = current_client.client_socket.recv(1024)
            message = decrypt_message(enc_message)

            print(comm)
            print(message)
            if not message:
                break
            if comm == FUNCS:
                if message.lower() == "help":
                    current_client.client_socket.send(encrypt_message(current_client, MSGBOX))
                    if current_client.admin:
                        current_client.client_socket.send(encrypt_message(current_client, admin_help_msg))
                    else:
                        current_client.client_socket.send(encrypt_message(current_client, help_msg))

                elif message.lower() == "get all usernames":
                    get_all_usernames()

                elif "make admin" in message.lower():
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

            elif message.lower().startswith("dm "):
                priv_chat(current_client, message)  # dm name:msg

            else:
                if not current_client.mute and approve_message_content(current_client, message):
                    # broadcast(CHAT, current_client)
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
    # set up the client's object and add it to the clients list
    current_client = Client(client_socket, "", admin, False, "")
    clients.append(current_client)

    # send if the user is an admin
    current_client.client_socket.send(str(admin).encode())

    # Send public key to client
    serialized_public_key = Encryptions_class.serialize_pub_key(public_key)
    client_socket.send(serialized_public_key)

    # get the client's public key
    serialized_client_pub_key = client_socket.recv(4096)
    client_pub_key = Encryptions_class.deserialize_pub_key(serialized_client_pub_key)
    current_client.rsa_pub_key = client_pub_key

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(current_client,))
    client_thread.start()
