#!/usr/bin/env python3
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def list_users_request(client_socket):
    client_socket.sendall("!users".encode())

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
        
        frame_widget = Frame(window)
        frame_widget.pack(padx=5, pady=5, fill=BOTH, expand=1)

        entry_widget = Entry(frame_widget)
        entry_widget.bind("<Return>", lambda _: send_message(client_socket, username, text_widget, entry_widget))
        entry_widget.pack(fill=BOTH, expand=1, side=LEFT)

        button_widget = Button(frame_widget, text="Send", command=lambda : send_message(client_socket, username, text_widget, entry_widget))
        button_widget.pack(side=RIGHT)
        

        users_widget = Button(window, text="List users", command=lambda : list_users_request(client_socket))
        users_widget.pack(padx=5, pady=5)

        thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
        thread.daemon = True
        thread.start()

        window.mainloop()

if __name__ == '__main__':
    client_program()
