"""
The login page to the program. Users may register to the program.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from UI import MainWindow
import DatabaseConnection as dc


# Start the login widow being handed the applications window object
def start(window, font_styles, photo):

    # Exit the program
    def exit_app():
        window.destroy()

    # Log into the program
    def login():

        if dc.login_user(username_entry.get(), password_entry.get(), dc.connect()):

            login_frame.pack_forget()
            window.minsize(1200, 800)  # Change the size of the window to a better size
            window.state('zoomed')  # maximize the window
            loading_bar = ttk.Progressbar(window, mode='determinate', length=500, maximum=100)
            loading_bar.pack(expand=True)
            loading_bar.step(30)
            loading_bar.update_idletasks()

            window.update()
            MainWindow.start(window, loading_bar)
        else:
            messagebox.showwarning("Login Error", "wrong username or password")

    # The login page
    login_frame = ttk.Frame(window, relief=tk.FLAT, borderwidth=5)
    login_frame.pack(pady=(50, 0))
    # Company logo
    img = tk.Label(login_frame, image=photo)
    img.pack(side='top')

    # Program name
    program_name = ttk.Label(login_frame, text='House Price Prediction Dashboard', style='ProgramName.Label')
    program_name.pack(pady=(0, 50))

    # Username field and entry
    username_field = ttk.Label(
        master=login_frame,
        text="username"
    )
    username_field.config(font=font_styles)
    username_entry = ttk.Entry(master=login_frame, width=30)
    username_field.pack()
    username_entry.pack(side="top")
    username_entry.insert(tk.END,'default')

    # Password field and entry
    password_field = ttk.Label(
        master=login_frame,
        text="password"
    )

    password_field.config(font=font_styles)
    password_entry = ttk.Entry(master=login_frame, show='*', width=30)
    password_field.pack()
    password_entry.pack(side="top")
    password_entry.insert(tk.END, 'default')

    # Login frame controls
    button_frame = ttk.Frame(master=login_frame, relief=tk.FLAT, borderwidth=5)
    button_frame.pack()

    # Exit button
    exit_btn = ttk.Button(master=button_frame, text="exit", command=exit_app)
    exit_btn.pack(side="left")

    # Login button
    login_btn = ttk.Button(master=button_frame, text="login", command=login)
    login_btn.pack(side="left")

    return window
