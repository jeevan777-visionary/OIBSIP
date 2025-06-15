# client.py
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 5000

nickname = simpledialog.askstring("Nickname", "Choose a nickname:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                chat_area.config(state=NORMAL)
                chat_area.insert(END, message + '\n')
                chat_area.config(state=DISABLED)
                chat_area.see(END)
        except:
            print("An error occurred.")
            client.close()
            break

def send():
    message = f"{nickname}: {msg_entry.get()}"
    client.send(message.encode('utf-8'))
    msg_entry.delete(0, END)

# GUI setup
window = Tk()
window.title("Chat App")

chat_area = ScrolledText(window)
chat_area.pack(padx=20, pady=5)
chat_area.config(state=DISABLED)

msg_entry = Entry(window)
msg_entry.pack(padx=20, pady=5, fill=X)

send_button = Button(window, text="Send", command=send)
send_button.pack(padx=20, pady=5)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

window.mainloop()