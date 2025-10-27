#!/usr/bin/env python3

import socket
import threading

def client_thread(client_socket, clients, usernames):
    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username
    
    print(f"[+] {username} has joined!")
    for client in clients:
        if client is not client_socket:
            client.sendall(f"\n[+] User {username} has joined the chat\n\n".encode())

    

def server_program():
    host = "localhost"
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()

        print("[+] Server is waiting for incoming connections")
        clients = []
        usernames = {}

        while True:

            client_socket, address = server_socket.accept()
            clients.append(client_socket)

            print(f"[+] A new client has joined: {address}")

            thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames))
            thread.daemon = True
            thread.start()
if __name__ == '__main__':
    server_program()
