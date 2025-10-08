# Chat Server

Este é um projeto simples de um chat em Python, utilizando sockets para a comunicação entre um servidor e múltiplos clientes.

## Tecnologias Utilizadas

- Python 3
- `socket`: Para a comunicação em rede.
- `threading`: Para permitir que o servidor lide com múltiplos clientes simultaneamente.
- `colorama`: Para colorir as mensagens no terminal.

## Como Rodar

### Servidor

Para iniciar o servidor, execute o seguinte comando no terminal:

```bash
python -m server.main
```

O servidor estará escutando na porta `5555` por padrão.

### Cliente

Para conectar um cliente ao servidor, execute o seguinte comando em um novo terminal:

```bash
python -m client.main
```

Você será solicitado a escolher um nome de usuário e, em seguida, poderá enviar e receber mensagens.