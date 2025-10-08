import socket
import threading
from colorama import Fore, init

init(autoreset=True)

clients = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket, address):
    print(Fore.GREEN + f"[+] Nova conexão de {address}")
    try:
        nickname = client_socket.recv(1024).decode()
    except:
        client_socket.close()
        return

    welcome = f"{nickname} entrou no chat!"
    print(Fore.CYAN + welcome)
    broadcast(welcome.encode())

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(Fore.WHITE + f"{nickname}: {message.decode()}")
            broadcast(f"{nickname}: {message.decode()}".encode(), client_socket)
        except:
            break

    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)
    broadcast(f"{nickname} saiu do chat.".encode())
    print(Fore.RED + f"[-] Conexão encerrada: {address}")

def start_server(host='127.0.0.1', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(Fore.YELLOW + f"[SERVIDOR] Escutando em {host}:{port}")

    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    start_server()