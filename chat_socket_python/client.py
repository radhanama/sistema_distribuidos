from socket import socket
from threading import Thread


def messages(connection: socket):

    while True:
        msg = connection.recv(1024)
        if msg:
            print(msg.decode())
        else:
            connection.close()
            break


def client() -> None:

    server_ip = '127.0.0.1'
    server_port = 12000

    try:
        socket_instance = socket()
        socket_instance.connect((server_ip, server_port))
        Thread(target=messages, args=[socket_instance]).start()

        print('Conectado!')

        while True:
            msg = input()

            if msg == 'sair':
                break

            socket_instance.send(msg.encode())

        socket_instance.close()

    except Exception as e:
        print(f'Erro ao conectar {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()
