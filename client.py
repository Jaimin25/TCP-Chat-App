import socket

ADDRESS = "localhost"

def start_client():
    PORT = input("ENTER PORT NUMBER: ")

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
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ADDRESS, PORT))

    while True:
        message = input("Client: ")
        client_socket.send(message.encode())

        if message.lower() == "exit()":
            print(f"Disconnecting...")
            break;

        response = client_socket.recv(1024).decode();
        print(f"Server: {response}")

if __name__ == "__main__":
    start_client();