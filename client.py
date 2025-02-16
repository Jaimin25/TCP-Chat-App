import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Chat")
        self.client_socket = None
        self.running = False
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()
        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=5)
        self.chat_display = scrolledtext.ScrolledText(root, state='disabled', width=50, height=15)
        self.chat_display.pack(pady=10)
        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.pack(pady=5)
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)
        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(pady=5)
    
    def connect_to_server(self):
        if self.running:
            messagebox.showwarning("Warning", "Already connected!")
            return
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Error", "Username is required!")
            return
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("127.0.0.1", 8888))
            self.client_socket.send((username + " joined the chat!").encode("utf-8"))
            self.running = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f"Connected to 127.0.0.1:8888 as {username}\n")
            self.chat_display.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if not message:
                    break
                self.chat_display.config(state='normal')
                
                self.chat_display.insert(tk.END, message + "\n")
                self.chat_display.config(state='disabled')
                self.chat_display.yview(tk.END)
            except ConnectionResetError:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, "Server disconnected.\n")
                self.chat_display.config(state='disabled')
                self.running = False
                break
    
    def send_message(self):
        if not self.running:
            messagebox.showerror("Error", "Not connected to any server!")
            return
        message = self.message_entry.get().strip()
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, str(self.username_entry.get())+"(You): "+ message + "\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)
        if message:
            try:
                self.client_socket.send((str(self.username_entry.get())+": "+ message).encode("utf-8"))
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Message sending failed: {e}")
    
    def disconnect(self):
        if not self.running:
            messagebox.showwarning("Warning", "Already disconnected!")
            return
        self.running = False
        self.client_socket.close()
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "Disconnected from server.\n")
        self.chat_display.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
