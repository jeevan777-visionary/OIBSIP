
import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Password length must be a positive integer.")
        return

    use_letters = var_letters.get()
    use_numbers = var_numbers.get()
    use_symbols = var_symbols.get()

    if not (use_letters or use_numbers or use_symbols):
        messagebox.showwarning("Input Error", "Select at least one character type.")
        return

    char_set = ""
    if use_letters:
        char_set += string.ascii_letters
    if use_numbers:
        char_set += string.digits
    if use_symbols:
        char_set += string.punctuation

    password = ''.join(random.choice(char_set) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# GUI setup
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")

tk.Label(root, text="Password Length:", font=("Arial", 12)).pack(pady=5)
length_entry = tk.Entry(root, font=("Arial", 12))
length_entry.pack(pady=5)

# Options
var_letters = tk.BooleanVar(value=True)
var_numbers = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=var_letters, font=("Arial", 10)).pack()
tk.Checkbutton(root, text="Include Numbers", variable=var_numbers, font=("Arial", 10)).pack()
tk.Checkbutton(root, text="Include Symbols", variable=var_symbols, font=("Arial", 10)).pack()

tk.Button(root, text="Generate Password", command=generate_password, font=("Arial", 12)).pack(pady=10)

password_entry = tk.Entry(root, font=("Arial", 12), width=30)
password_entry.pack(pady=5)

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=("Arial", 12)).pack(pady=10)

root.mainloop()
