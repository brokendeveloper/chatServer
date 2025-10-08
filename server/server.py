import socket
import threading
import time
from colorama import Fore, Style, init

init(autoreset=True)


class Server:
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.colors = [Fore.BLUE, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Fore.RED]
        self.lock = threading.Lock()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.log(f"Servidor iniciado em {self.host}:{self.port}")

    def log(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(f"{Style.BRIGHT}{Fore.WHITE}[{timestamp}] {message}")

    def get_client_color(self, client):
        with self.lock:
            if client in self.clients:
                index = self.clients.index(client)
                return self.colors[index % len(self.colors)]
        return Fore.WHITE

    def broadcast(self, message, sender_client=None):
        with self.lock:
            for client in self.clients:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)

    def remove_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            nickname = self.nicknames[index]

            self.clients.remove(client)
            self.nicknames.pop(index)

            self.log(f"{Fore.YELLOW}Desconexão: {nickname} saiu do chat.")
            self.broadcast(f"{Fore.YELLOW}{nickname} saiu do chat.".encode('utf-8'))

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if not message:
                    with self.lock: self.remove_client(client)
                    break

                sender_color = self.get_client_color(client)
                formatted_message = sender_color + message.decode('utf-8')

                self.log(f"Mensagem recebida: {message.decode('utf-8')}")
                self.broadcast(formatted_message.encode('utf-8'))

            except Exception as e:
                self.log(f"{Fore.RED}[ERRO] Erro com o cliente: {e}")
                with self.lock:
                    self.remove_client(client)
                break

    def start(self):
        while True:
            try:
                client, address = self.server_socket.accept()
                self.log(f"{Fore.GREEN}[CONEXÃO] Nova conexão de {address}")

                client.send('NICK'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')

                with self.lock:
                    self.nicknames.append(nickname)
                    self.clients.append(client)
                    client_color = self.get_client_color(client)

                self.log(f"Nickname do cliente é {client_color}{nickname}")
                self.broadcast(f"{client_color}{nickname} entrou no chat!".encode('utf-8'))
                client.send(f"{Fore.GREEN}Conectado ao servidor!".encode('utf-8'))

                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()
            except KeyboardInterrupt:
                self.log("Servidor sendo desligado.")
                self.server_socket.close()
                break
            except Exception as e:
                self.log(f"{Fore.RED}[ERRO] Erro ao aceitar conexões: {e}")