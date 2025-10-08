import socket
import threading
from colorama import Fore, init

init(autoreset=True)

class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.nickname = input("Escolha seu nome: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            self.client.send(self.nickname.encode())
            self.connected = True
            print(Fore.GREEN + "Conectado ao servidor!")
        except Exception as e:
            print(Fore.RED + f"Erro ao conectar: {e}")
            self.connected = False

    def receive(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode()
                if message:
                    print(message)
                else:
                    break
            except:
                print(Fore.RED + "Conexão perdida com o servidor.")
                self.client.close()
                self.connected = False
                break

    def write(self):
        while self.connected:
            message = input("")
            if message.lower() == "/sair":
                self.client.close()
                self.connected = False
                break
            self.client.send(message.encode())

    def start(self):
        self.connect()
        if not self.connected:
            return

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    client = Client()
    client.start()