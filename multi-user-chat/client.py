#!/usr/bin/env python3
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def receive_message(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break
            text_widget.configure(state='normal')
            text_widget.insert(END, message)
            text_widget.configure(state='disabled')


        except:
            break

def send_message(client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f"{username} > {message}\n".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username} > {message}\n")
    text_widget.configure(state='disabled')

def client_program():
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        username = input("username: ")
        client_socket.sendall(username.encode())
        window = Tk()
        window.title("Chat")
        
        text_widget = ScrolledText(window, state='disabled')
        text_widget.pack(padx=10, pady=10)

        entry_widget = Entry(window)
        entry_widget.bind("<Return>", lambda _: send_message(event, client_socket, username, text_widget, entry_widget))
        entry_widget.pack(pady=5, padx=5, fill=BOTH)
        thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
        thread.daemon = True
        thread.start()

        window.mainloop()

if __name__ == '__main__':
    client_program()
