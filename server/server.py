import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

lock = threading.Lock()

def broadcast(message, _client=None):
    with lock:
        for client in clients:
            if client != _client:
                try:
                    client.send(message)
                except:
                    remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast(f'{nickname} saiu do chat.'.encode('utf-8'))
        print(f'{nickname} desconectado.')

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                with lock:
                    remove_client(client)
                break
            broadcast(message, client)
        except:
            with lock:
                remove_client(client)
            break

def receive_connections():
    print("Servidor está online e aguardando conexões...")
    while True:
        client, address = server.accept()
        print(f"Nova conexão de {str(address)}")
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        with lock:
            nicknames.append(nickname)
            clients.append(client)
        print(f"Nome do cliente é {nickname}")
        broadcast(f"{nickname} entrou no chat!".encode('utf-8'), client)
        client.send("Conectado ao servidor!".encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive_connections()
