import tkinter as tk
from tkinter import scrolledtext, messagebox


class Gui1:
    def __init__(self, login_func, send_msg_func, recv_msgs_func):
        self.root = tk.Tk()
        self.root.title("Welcome")
        self.root.geometry("350x550")
        self.login_func = login_func
        self.send_msg_func = send_msg_func
        self.recv_msgs_func = recv_msgs_func

    def signin_and_signup_buttons(self):
        # Create a frame for the message
        message_frame = tk.Frame(self.root)
        message_frame.pack(pady=10)

        # Create a label for the message
        message_label = tk.Label(message_frame, text="Welcome to the Page", font=("Arial", 16))
        message_label.pack()

        # Create a frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=50)

        # Create the first button and place it in the button frame
        button1 = tk.Button(button_frame, text="Sign up", command=lambda: self.open_sign_in_window("Sign up"), width=15, height=3, font=("Arial", 12))
        button1.grid(row=0, column=0, padx=10)

        # Create the second button and place it in the button frame
        button2 = tk.Button(button_frame, text="Sign in", command=lambda: self.open_sign_in_window("Sign in"), width=15, height=3, font=("Arial", 12))
        button2.grid(row=0, column=1, padx=10)

    def open_sign_in_window(self, comm):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        sign_in_label = tk.Label(self.root, text=f"{comm} Page")
        sign_in_label.pack(pady=10)

        username_label = tk.Label(self.root, text="Username:")
        username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        if comm == "Sign in":
            login_button = tk.Button(self.root, text="Sign in", command=self.on_login_button_click)
            login_button.pack(pady=10)
        else:
            login_button = tk.Button(self.root, text="Sign up", command=self.on_signup_button_click)
            login_button.pack(pady=10)

    def on_login_button_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_func(username, password)

    def on_signup_button_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_func(username, password)

    def chat_window(self, username):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, width=40, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Message entry field
        self.message_entry = tk.Entry(self.root, width=30)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", width=10, command=lambda: self.send_message(username))
        self.send_button.grid(row=1, column=1, padx=10, pady=5)

        self.chat_display.config(state=tk.DISABLED)  # Disable editing of chat display

    def send_message(self, username):
        message = self.message_entry.get()
        if message:
            # message = f"{username}: {message}"
            self.display_message(message)
            self.message_entry.delete(0, tk.END)
            self.send_msg_func(message)
        else:
            messagebox.showwarning("Empty Message", "Please enter a message.")

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)  # Enable editing of chat display
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.see(tk.END)  # Scroll to the bottom of the chat display
        self.chat_display.config(state=tk.DISABLED)  # Disable editing of chat display

