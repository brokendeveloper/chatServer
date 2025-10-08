import socket
import threading
from colorama import init, Fore, Style

init(autoreset=True)


class Client:
    def __init__(self, host='127.0.0.1', port=55555):
        self.nickname = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def print_welcome_message(self):
        print(Fore.CYAN + Style.BRIGHT + "=========================================")
        print(Fore.CYAN + Style.BRIGHT + " Bem-vindo ao Chat Distribuído!")
        print(Fore.CYAN + Style.BRIGHT + "=========================================")
        print("Conectando ao servidor...")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print(Fore.RED + "Você foi desconectado do servidor.")
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            try:
                message = input("")
                full_message = f'{self.nickname}: {message}'
                self.client_socket.send(full_message.encode('utf-8'))
            except EOFError:
                self.client_socket.close()
                break
            except:
                break

    def start(self):
        self.print_welcome_message()
        self.nickname = input("Escolha seu nome: ")

        try:
            self.client_socket.connect((self.host, self.port))
        except:
            print(Fore.RED + "Não foi possível conectar ao servidor.")
            return

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_messages()