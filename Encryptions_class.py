from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


# Generate RSA key pair
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


# def encrypt_pubkey_64(pem_format):
#     encoded_public_key = base64.b64encode(pem_format)
#     return encoded_public_key
#
#
# def decrypt_pubkey_64(encoded_public_key):
#     decoded_public_key_bytes = base64.b64decode(encoded_public_key)
#     return decoded_public_key_bytes


# Encrypt message
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


# Decrypt message
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


def serialize_pub_key(public_key):
    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return serialized_public_key


def deserialize_pub_key(serialized_pub_key):
    public_key = serialization.load_pem_public_key(
        serialized_pub_key,
        backend=default_backend()
    )
    return public_key


