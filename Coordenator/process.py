from socket import socket
from threading import Thread
from time import sleep
import datetime

class Processo:
    """A class that connects to a coordenator and requests to write to a file a number of times

    Args:
        k (int): Number of seconds the process waits before relaeasing sending releasing access.
        r (int): Number of times the process requests access.
    """

    def __init__(self,k =1,r = 5) -> None:
        self.__k= k
        self.__r = r
        self.grants = 0
    
    def __messages(self,connection: socket):
        connection.send("REQUEST".encode())
        while True:
            msg = connection.recv(1024)
            if msg:
                if msg.decode() == "GRANT":
                    self.grants += 1
                    with open("resultado.txt", "a") as file:
                        file.write(f"{connection.getsockname()[1]} - {datetime.datetime.now()}\n")
                    sleep(self.__k)
                    connection.send("RELEASE".encode())
                    if self.grants == self.__r:
                        connection.close()
                        break
                    else:
                        connection.send("REQUEST".encode())
    

        
    def __client(self) -> None:

        server_ip = '127.0.0.1'
        server_port = 12000

        try:
            socket_instance = socket()
            socket_instance.connect((server_ip, server_port))
            print('Conectado!')
            Thread(target=self.__messages, args=[socket_instance]).start()
        except Exception as e:
            print(f'Erro ao conectar {e}')
            socket_instance.close()


    def run(self) -> None:
        """Runs the process"""
        self.__client()


def run_processes():
    """Runs a number of processes simultaneously"""
    processes = [Processo(), Processo(), Processo()]
    for process in processes:
        Thread(target=process.run, args=[]).start()

run_processes()
