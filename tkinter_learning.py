import tkinter as tk
from tkinter import messagebox

import tkinter as tk

def get_input():
    # Perform some operations to get input
    return "input_value"

def button_callback():
    result = get_input()
    print("Returned value:", result)

root = tk.Tk()

# Create a button that calls the function when clicked
button = tk.Button(root, text="Get Input", command=button_callback)
button.pack()


root.mainloop()

# def log_in():
#     username = username_entry.get()
#     password = password_entry.get()
#
#     # Replace this with your authentication logic
#     if username == "admin" and password == "password":
#         messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
#     else:
#         messagebox.showerror("Login Failed", "Invalid username or password")
#
# # Create the main window
# root = tk.Tk()
# root.title("moriya's project")
#
# root.geometry("350x550")
#
# # Create username label and entry
# username_label = tk.Label(root, text="Username:")
# username_label.grid(row=0, column=0, padx=5, pady=5)
# username_entry = tk.Entry(root)
# username_entry.grid(row=0, column=1, padx=5, pady=5)
#
# # Create password label and entry
# password_label = tk.Label(root, text="Password:")
# password_label.grid(row=1, column=0, padx=5, pady=5)
# password_entry = tk.Entry(root, show="*")
# password_entry.grid(row=1, column=1, padx=5, pady=5)

# Create login button
# login_button = tk.Button(root, text="Login",  width=15, height=3, font=("Ariel", 12), bg="pink")
# login_button.grid(padx=100, pady=200)

# Run the main loop
root.mainloop()
#
# import tkinter as tk
#
# def open_signup_window():
#     clear_main_window()
#     signup_label = tk.Label(root, text="Signup Page")
#     signup_label.pack(pady=10)
#     # Add your signup window content here
#
# def open_sign_in_window():
#     clear_main_window()
#     sign_in_label = tk.Label(root, text="Signin Page")
#     sign_in_label.pack(pady=10)
#
#     global username_entry, password_entry
#     username_label = tk.Label(root, text="Username:")
#     username_label.pack()
#     username_entry = tk.Entry(root)
#     username_entry.pack(pady=5)
#
#     password_label = tk.Label(root, text="Password:")
#     password_label.pack()
#     password_entry = tk.Entry(root, show="*")
#     password_entry.pack(pady=5)
#
#     login_button = tk.Button(root, text="Login")
#     login_button.pack(pady=10)
#
# def clear_main_window():
#     for widget in root.winfo_children():
#         widget.destroy()
#
# # Create the main window
# root = tk.Tk()
# root.title("Welcome")
# root.geometry("350x550")
#
# # Create signup button
# signup_button = tk.Button(root, text="Signup", command=open_signup_window)
# signup_button.pack(pady=10)
#
# # Create signin button
# signin_button = tk.Button(root, text="Signin", command=open_sign_in_window)
# signin_button.pack(pady=10)
#
# # Run the main loop


# root = tk.Tk()
# root.title("Welcome")
# root.geometry("350x550")
#
# def open_sign_in_or_up_window(command):
#     clear_main_window()
#     sign_in_label = tk.Label(root, text=f"{command} Page")
#     sign_in_label.pack(pady=10)
#
#     # global username_entry, password_entry
#     username_label = tk.Label(root, text="Username:")
#     username_label.pack()
#     username_entry = tk.Entry(root)
#     username_entry.pack(pady=5)
#
#     password_label = tk.Label(root, text="Password:")
#     password_label.pack()
#     password_entry = tk.Entry(root, show="*")
#     password_entry.pack(pady=5)
#
#     login_button = tk.Button(root, text=f"{command}")
#     login_button.pack(pady=10)
#
#     return username_entry, password_entry
#
# def clear_main_window():
#     for widget in root.winfo_children():
#         widget.destroy()
#
#
# # Create signup button
# signup_button = tk.Button(root, text="Signup", command=lambda: open_sign_in_or_up_window("Sign up"))
# signup_button.pack(pady=10)
#
# # Create signin button
# signin_button = tk.Button(root, text="Signin", command=lambda: open_sign_in_or_up_window("Sign in"))
# signin_button.pack(pady=10)
#
# root.mainloop()


