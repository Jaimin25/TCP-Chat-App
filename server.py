import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatServer:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Chat")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", 8888))
        self.server_socket.listen(1)
        self.clients = []
        threading.Thread(target=self.accept_clients, daemon=True).start()
        self.chat_display = scrolledtext.ScrolledText(root, state='disabled', width=50, height=15)
        self.chat_display.pack(pady=10)
    
    def accept_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
    
    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    break
                self.broadcast(message, client_socket)
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break
    
    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                client.send(message.encode("utf-8"))
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, message + "\n")
                self.chat_display.config(state='disabled')
                self.chat_display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    server = ChatServer(root)
    root.mainloop()
