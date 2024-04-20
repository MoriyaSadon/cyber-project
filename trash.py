import tkinter as tk
from tkinter import scrolledtext, messagebox


class ChatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat App")

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Message entry field
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", width=10, command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=5)

        self.chat_display.config(state=tk.DISABLED)  # Disable editing of chat display

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.display_message(f"You: {message}")
            self.message_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Message", "Please enter a message.")

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)  # Enable editing of chat display
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.see(tk.END)  # Scroll to the bottom of the chat display
        self.chat_display.config(state=tk.DISABLED)  # Disable editing of chat display

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatApp()
    app.run()





# def validate_login():
#     # Retrieve the entered username and password
#     entered_username = username_entry.get()
#     entered_password = password_entry.get()
#
#     # Check if the username is correct (for demonstration, let's assume the correct username is "user")
#     if entered_username == "user":
#         # Check if the password is correct (for demonstration, let's assume the correct password is "password")
#         if entered_password == "password":
#             messagebox.showinfo("Login Successful", "Welcome, User!")
#         else:
#             # If the password is wrong, prompt the user to enter a new password
#             messagebox.showwarning("Invalid Password", "Incorrect password. Please enter a new password.")
#             # password_entry.delete(0, tk.END)  # Clear the password entry field
#     else:
#         # If the username is wrong, prompt the user to enter a new username
#         messagebox.showwarning("Invalid Username", "Incorrect username. Please enter a new username.")
#         # username_entry.delete(0, tk.END)  # Clear the username entry field
#
# # Create the main window
# root = tk.Tk()
# root.title("Login")
#
# # Username label and entry field
# username_label = tk.Label(root, text="Username:")
# username_label.grid(row=0, column=0, padx=10, pady=5)
# username_entry = tk.Entry(root)
# username_entry.grid(row=0, column=1, padx=10, pady=5)
#
# # Password label and entry field
# password_label = tk.Label(root, text="Password:")
# password_label.grid(row=1, column=0, padx=10, pady=5)
# password_entry = tk.Entry(root, show="*")
# password_entry.grid(row=1, column=1, padx=10, pady=5)
#
# # Login button
# login_button = tk.Button(root, text="Login", command=validate_login)
# login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
#
# # Run the main event loop
# root.mainloop()





# from cryptography.hazmat.primitives import padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
#
# key = b'my_secret_key123'
# iv = b'initialize_vec'
#
# # Create AES cipher object
# cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#
# # Create padding object
# padder = padding.PKCS7(algorithms.AES.block_size).padder()
# unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#
# # Function to encrypt plaintext
# def encrypt(plaintext):
#     encryptor = cipher.encryptor()
#     padded_plaintext = padder.update(plaintext) + padder.finalize()
#     ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
#     return ciphertext
#
# # Function to decrypt ciphertext
# def decrypt(ciphertext):
#     decryptor = cipher.decryptor()
#     padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
#     plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
#     return plaintext



# admin only
# def add_remove_from_censored_table(my_client: Client, msg, word):
#     data_dict = {"word": word}
#     if my_client.admin:
#         if "add" in msg:
#             censored_table.add_data(data_dict)
#             my_client.client_socket.send("*** the word was added successfully ***".encode())
#         else:
#             censored_table.remove_data(data_dict)
#             my_client.client_socket.send("*** the word was removed successfully ***".encode())
#     else:
#         my_client.client_socket.send("you're not an admin therefore you cant do that".encode())


# if "add censored word" or "remove censored word" in message:
            #     word = message.split(":")[1]  # add/remove:word
            #     add_remove_from_censored_table(current_client, message, word)


# db_conn = Censored_db.create_connection()
# db_cursor = Censored_db.create_table(db_conn)

# db tables
# censored_table = database_class.Database("censored")

# import Encryptions_class
# import base64
#
# message = "Log in by entering your username"
#
# pub, priv = Encryptions_class.generate_keys_rsa()
#
# en_pub = Encryptions_class.encrypt_pubkey_64(pub)
#
# dec_pub = Encryptions_class.decrypt_pubkey_64(en_pub)
#
# en_msg = Encryptions_class.encrypt_msg_rsa(message, dec_pub)
#
# dec_msg = Encryptions_class.decrypt_msg_rsa(en_msg, priv)
#
# print(dec_msg)



# לעשות מפתחות לסרבר, קליינט שולח הודעה מוצפנת עם המפתח של הסרבר לסרבר, הסרבר מפענח, לוקח את המפתחות הציבוריים של כל אחד מהקליינטים ושולח להם, הקליינטים מפענחים עם המפתחות הפרטיים שלהם
