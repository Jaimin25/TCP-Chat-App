import socket

ADDRESS = "localhost"

def start_server():
    PORT = input("Enter port (must be a number): ")

    if not PORT or not PORT.isdigit():
        print("Port invalid!")
        return
    
    PORT = int(PORT)
    
    if not PORT > 0:
        print("Invalid port number")
        return
    
    if PORT < 1024:
        print(f"{PORT} is a reserved port number, please try again")
        return

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((ADDRESS, PORT))
    socket_server.listen(10)

    print(f"Server is running: {ADDRESS}:{PORT}\n")

    client_socket, client_address = socket_server.accept()

    print(f"Connected established with {client_address}\n")

    while True:
        message = client_socket.recv(1024).decode()

        if message.lower() == "exit()":
            print(f"Client {client_address} disconnect")
            break
            
        print(f"Client: {message}")

        response = input("Server: ")
        client_socket.send(response.encode())

if __name__ == "__main__":
    start_server();