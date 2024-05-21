from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

class RsaEnc:
    def __init__(self, pub_key, priv_key):
        self.KEY_SIZE = 2048
        self.pub_key = pub_key
        self.priv_key = priv_key

    # Generate RSA key pair
    def generate_key_pair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.KEY_SIZE,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        self.pub_key = public_key
        self.priv_key = private_key

    # Encrypt message
    def encrypt_message(self, message):
        encrypted_message = self.pub_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        b64_encoded = base64.b64encode(encrypted_message)
        return b64_encoded

    # Decrypt message
    def decrypt_message(self, b64_encoded):
        encrypted_message = base64.b64decode(b64_encoded)

        decrypted_message = self.priv_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()

    # change the type of the key to bytes
    def serialize_pub_key(self):
        serialized_public_key = self.pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return serialized_public_key

    # change the key type from bytes
    def deserialize_pub_key(self, serialized_pub_key):
        public_key = serialization.load_pem_public_key(
            serialized_pub_key,
            backend=default_backend()
        )
        self.pub_key = public_key


