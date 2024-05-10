
class Client:
    def __init__(self, client_socket, name, admin, mute, rsa_pub_key):
        self.client_socket = client_socket
        self.name = name
        self.admin = admin  # t/f
        self.mute = mute  # t/f
        self.rsa_pub_key = rsa_pub_key










