import socket
from threading import Thread

conections = []

messages = []


def user_connection(connection: socket.socket, address):
    for message in messages:
        connection.send(message.encode())
    while True:
        msg = connection.recv(1024)

        if msg:
            messages.append(f'{address[0]}:{address[1]}: {msg.decode()}')

            msg_to_send = f'{address[0]}:{address[1]}: {msg.decode()}'
            broadcast(msg_to_send, connection)

        else:
            remove_connection(connection)
            break


def broadcast(message, connection: socket.socket):

    for client_conn in conections:
        if client_conn != connection:
            try:
                client_conn.send(message.encode())

            except Exception as e:
                print(f'Erro ao enviar mensagem para todos: {e}')
                remove_connection(client_conn)


def remove_connection(conn: socket.socket):

    if conn in conections:
        conn.close()
        conections.remove(conn)


def server():
    PORTA = 12000

    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', PORTA))
        socket_instance.listen(4)

        print('Server conectado!')

        while True:

            socket_conection, address = socket_instance.accept()
            conections.append(socket_conection)
            Thread(target=user_connection, args=[
                             socket_conection, address]).start()

    except Exception as e:
        print(f'erro ao instaciar o socket: {e}')


if __name__ == "__main__":
    server()
