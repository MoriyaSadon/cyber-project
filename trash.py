import Encryptions_class

username = "shira"
msg = f"{username} is now an admin"

priv, pub = Encryptions_class.generate_key_pair()
enc = Encryptions_class.encrypt_message(msg, pub)
dec = Encryptions_class.decrypt_message(enc, priv)
print(dec)


# def encrypt_large_message(large_message, public_key):
#     chunks = []
#     max_length = (KEY_SIZE // 8) - 2 * 32 - 2
#     for i in range(0, len(large_message), max_length):
#         chunk = large_message[i:i + max_length]
#         enc_chunk = encrypt_message(chunk, public_key)
#         chunks.append(enc_chunk)
#     return chunks
#
# def decrypt_large_message(chunks_lst, private_key):
#     message = ""
#     for i in chunks_lst:
#         chunk = decrypt_message(i, private_key)
#         message += chunk
#     return message

# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import serialization, hashes
# from cryptography.hazmat.primitives.asymmetric import padding, rsa
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# import os
#
# # Generate RSA key pair
# def generate_key_pair():
#     private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048,
#         backend=default_backend()
#     )
#     public_key = private_key.public_key()
#     return private_key, public_key
#
# # Generate a random symmetric key
# def generate_symmetric_key():
#     return os.urandom(32)  # 32 bytes for AES-256
#
# # Encrypt large message
# def encrypt_large_message(message, public_key):
#     # Generate a random symmetric key
#     symmetric_key = generate_symmetric_key()
#
#     # Encrypt the large message with symmetric encryption (AES)
#     iv = os.urandom(16)  # Initialization vector for AES
#     cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
#     ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
#
#     # Encrypt the symmetric key with asymmetric encryption (RSA)
#     encrypted_symmetric_key = public_key.encrypt(
#         symmetric_key,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#
#     # Return the encrypted symmetric key and the ciphertext
#     return encrypted_symmetric_key, iv, ciphertext
#
# # Decrypt large message
# def decrypt_large_message(encrypted_symmetric_key, iv, ciphertext, private_key):
#     # Decrypt the symmetric key with asymmetric decryption (RSA)
#     symmetric_key = private_key.decrypt(
#         encrypted_symmetric_key,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#
#     # Decrypt the large message with symmetric decryption (AES)
#     cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
#
#     return decrypted_message.decode()
#
# # Example usage
# # private_key, public_key = generate_key_pair()
# # encrypted_symmetric_key, iv, ciphertext = encrypt_large_message("Your large message here", public_key)
# # decrypted_message = decrypt_large_message(encrypted_symmetric_key, iv, ciphertext, private_key)
