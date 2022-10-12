from multiprocessing import Semaphore
import socket
from threading import Thread, Event


conections = []
mutex = Semaphore(1)
accept_list = []

class Connection(Thread): 
    

    def __init__(self, connection, address, mutex, event) -> None:
        Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.mutex = mutex
        self.event = event
        
    def user_connection(self):
        print(f"CONNECT {self.address[1]}")
        while True:
            msg = self.connection.recv(7)

            if msg:
                mutex.acquire()
                if msg.decode() == "REQUEST":
                    print(f"REQUEST {self.address[1]}")
                    if len(accept_list) == 0 and self.event.is_set():
                        print(f"GRANT  {self.address[1]}")
                        self.event.clear()
                        Connection.send_message("GRANT", self.connection)
                    else:
                        accept_list.append((self.connection,self.address))
                    # mutex.release()

                if msg.decode() == "RELEASE":
                    # mutex.acquire()
                    print(f"RELEASE {self.address[1]}")
                    self.event.set()
                    if len(accept_list) != 0  and self.event.is_set():
                        self.event.clear()
                        actual_connection = accept_list.pop(0)
                        print(f"GRANT  {actual_connection[1][1]}")
                        Connection.send_message("GRANT", actual_connection[0])
                mutex.release()
         
            else:
                print(f"EXIT {self.address[1]}")
                remove_connection(self.connection)
                break
    
    def run(self):
        self.user_connection()
    
    @staticmethod
    def send_message(message, client_conn):
        client_conn.send(message.encode())

def remove_connection(conn: socket.socket):

    if conn in conections:
        conn.close()
        conections.remove(conn)


def server():
    PORTA = 12000
    ...

    event = Event()
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', PORTA))
        socket_instance.listen(10)

        print('Server conectado!')
        event.set()
        while True:

            socket_connection, address = socket_instance.accept()
            thread = Connection(socket_connection,address,mutex, event).start()

    except Exception as e:
        print(f'erro ao instaciar o socket: {e}')


if __name__ == "__main__":
    server()
