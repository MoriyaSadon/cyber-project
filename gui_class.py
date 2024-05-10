import tkinter as tk
from tkinter import scrolledtext, messagebox


class Gui1:
    def __init__(self, admin_mode, login_func, signup_func, send_chat_msg_func, send_funcs_msg_func, help_guide_func, send_priv_msg_func):
        self.root = tk.Tk()
        self.root.title("Welcome")
        self.root.geometry("350x570")
        self.admin_mode = admin_mode
        self.login_func = login_func
        self.signup_func = signup_func
        self.send_chat_msg_func = send_chat_msg_func
        self.send_funcs_msg_func = send_funcs_msg_func
        self.help_guide_func = help_guide_func
        self.send_priv_msg_func = send_priv_msg_func

    # create the signin and signup buttons in the start page
    def signin_and_signup_buttons(self):
         # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame for the message
        message_frame = tk.Frame(self.root)
        message_frame.pack(pady=10)

        # Create a label for the message
        message_label = tk.Label(message_frame, text="Welcome to SAFE SPACE", font=("Arial", 16))
        message_label.pack()

        # Create a frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=50)

        # Create the first button and place it in the button frame
        button1 = tk.Button(button_frame, text="Sign up", command=lambda: self.open_signin_signup_window("Sign up"), width=15, height=3, font=("Arial", 12))
        button1.grid(row=0, column=0, padx=10)

        # Create the second button and place it in the button frame
        button2 = tk.Button(button_frame, text="Sign in", command=lambda: self.open_signin_signup_window("Sign in"), width=15, height=3, font=("Arial", 12))
        button2.grid(row=0, column=1, padx=10)

    # signup or signin pages
    def open_signin_signup_window(self, comm):
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
        elif comm == "Sign up":
            signup_button = tk.Button(self.root, text="Sign up", command=self.on_signup_button_click)
            signup_button.pack(pady=10)

        signup_button = tk.Button(self.root, text="back", command=self.signin_and_signup_buttons)
        signup_button.pack(pady=15)

    # login button to get to the chat
    def on_login_button_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.username_entry.delete(0, tk.END)  # Clear the username entry field
        self.password_entry.delete(0, tk.END)  # Clear the password entry field
        self.login_func(username, password)

    # signup gutton to get to the chat
    def on_signup_button_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.username_entry.delete(0, tk.END)  # Clear the username entry field
        self.password_entry.delete(0, tk.END)  # Clear the password entry field
        self.signup_func(username, password)

    # the main window used - the chat window
    def chat_window(self):
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
        self.send_button = tk.Button(self.root, text="Send", width=10, command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=5)

        self.chat_display.config(state=tk.DISABLED)  # Disable editing of chat display

        # functions buttons

        # help guide button
        self.help_button = tk.Button(self.root, text="help", width=15, command=self.help_guide_func)
        self.help_button.grid(row=2, column=1, padx=10, pady=5)

        # video call button
        self.video_call_button = tk.Button(self.root, text="video call", width=15)
        self.video_call_button.grid(row=2, column=0, padx=10, pady=5)

        # get usernames lst button
        self.users_lst_button = tk.Button(self.root, text="users in chat", width=15, command=lambda: self.send_funcs_msg_func("get all usernames"))
        self.users_lst_button.grid(row=3, column=0, padx=10, pady=5)

        # send private message
        self.users_lst_button = tk.Button(self.root, text="send private msg", width=15, command=self.new_window_for_priv_msg)
        self.users_lst_button.grid(row=3, column=1, padx=10, pady=5)

        if self.admin_mode:
            self.admin_buttons()

    # enter message and send it
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.display_message(message)
            self.message_entry.delete(0, tk.END)
            self.send_chat_msg_func(message)
        else:
            messagebox.showwarning("Empty Message", "Please enter a message.")

    # display a message
    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)  # Enable editing of chat display
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.see(tk.END)  # Scroll to the bottom of the chat display
        self.chat_display.config(state=tk.DISABLED)  # Disable editing of chat display

    # buttons for admins only
    def admin_buttons(self):
        # censored word button
        censored_word_button = tk.Button(self.root, text="edit censored words", width=15, command=self.new_window_for_censored_words)
        censored_word_button.grid(row=5, column=0, padx=10, pady=5)

        # mute button
        mute_button = tk.Button(self.root, text="mute users", width=15, command=lambda: self.new_window_for_mute_unmute("mute"))
        mute_button.grid(row=4, column=1, padx=10, pady=5)

        # unmute button
        unmute_button = tk.Button(self.root, text="unmute users", width=15, command=lambda: self.new_window_for_mute_unmute("unmute"))
        unmute_button.grid(row=4, column=0, padx=10, pady=5)

        # make admin button"
        make_admin_button = tk.Button(self.root, text="make admin", width=15, command=lambda: self.new_window_for_make_admin_or_kick("make admin"))
        make_admin_button.grid(row=5, column=1, padx=10, pady=5)

        # kick button"
        make_admin_button = tk.Button(self.root, text="kick a user", width=15, command=lambda: self.new_window_for_make_admin_or_kick("kick"))
        make_admin_button.grid(row=6, column=1, padx=10, pady=5)

    # send a message to a specific user (func from a button)
    def new_window_for_priv_msg(self):
        # Create the options window
        root_lil_window = tk.Tk()
        root_lil_window.title("private message")

        # Add labels, buttons, or other widgets to the custom dialog
        label = tk.Label(root_lil_window, text=f"enter the user you want to send the message to and the message")
        label.pack()

        username_label = tk.Label(root_lil_window, text="username")
        username_label.pack()
        username_entry = tk.Entry(root_lil_window)
        username_entry.pack(pady=5)

        message_label = tk.Label(root_lil_window, text="message")
        message_label.pack()
        message_entry = tk.Entry(root_lil_window)
        message_entry.pack(pady=5)

        submit_button = tk.Button(root_lil_window, text="send message", command=lambda: self.send_priv_msg_func(username_entry.get(), message_entry.get()))
        submit_button.pack(pady=5)

    # mute or unmute a specific user or everyone (func from buttons)
    def new_window_for_mute_unmute(self, comm):
        # Create the options window
        root_lil_window = tk.Tk()
        root_lil_window.title(comm)

        # Add labels, buttons, or other widgets to the custom dialog
        label = tk.Label(root_lil_window, text=f"who do you want to {comm}")
        label.pack()

        specific_button = tk.Button(root_lil_window, text="specific user", command=lambda: self.label_window(comm, root_lil_window))
        specific_button.pack(pady=10)

        if comm == "mute":
            specific_comm = "mute everyone"
        else:
            specific_comm = "unmute everyone"

        everyone_button = tk.Button(root_lil_window, text="everyone", command=lambda: self.send_funcs_msg_func(specific_comm))
        everyone_button.pack(pady=5)

    # edit the censored words list - add or remove (func from a button)
    def new_window_for_censored_words(self):
        # Create the options window
        root = tk.Tk()
        root.title("censored word")

        # Add labels, buttons, or other widgets to the custom dialog
        label = tk.Label(root, text=f"do you want to add or remove a word?")
        label.pack()

        btn_ok = tk.Button(root, text="add word", command=lambda: self.label_window("add censored word", root))
        btn_ok.pack(pady=10)

        btn_cancel = tk.Button(root, text="remove word", command=lambda: self.label_window("remove censored word", root))
        btn_cancel.pack(pady=5)

    # make a user an admin or kick a user (func from buttons)
    def new_window_for_make_admin_or_kick(self, comm):
        # Create the options window
        root = tk.Tk()
        root.title(comm)
        self.label_window(comm, root)

    # make the new window to enter the wanted data - entry and a button to submit
    def label_window(self, comm, root):
        # Clear window
        for widget in root.winfo_children():
            widget.destroy()

        if comm == "mute" or comm == "unmute" or comm == "make admin" or comm == "kick":
            label = "enter username"
        else:
            label = "enter word"
        ans_label = tk.Label(root, text=label)
        ans_label.pack()
        self.ans_entry = tk.Entry(root)
        self.ans_entry.pack(pady=5)

        submit_button = tk.Button(root, text="submit", command=lambda: self.submit(comm))
        submit_button.pack(pady=5)

    # sends the data that was entered to the server (with a func from the client)
    def submit(self, comm):
        msg = f"{comm}:{self.ans_entry.get()}"
        self.send_funcs_msg_func(msg)

