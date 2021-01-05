"""
A program to help the company predict house prices so that we can invest into them and make money.
"""
import tkinter as tk
from tkinter import ttk
from UI import Login
import os

if __name__ == '__main__':
    # Create the window
    window = tk.Tk()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    photo_path = os.path.join(current_directory, "photos\\mccore_icon.png")
    # Set the title
    window.title("McCore Investing LLC - House Price Prediction Dashboard")
    window.minsize(500, 300)
    photo = tk.PhotoImage(file=photo_path)
    window.iconphoto(False, photo)

    # style settings
    font_styles = ("Arial", 12)
    style = ttk.Style()
    style.configure("ProgramName.Label", font=('Arial', 18))

    Login.start(window, font_styles, photo)

    window.mainloop()

