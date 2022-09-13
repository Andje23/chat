import time
import socket
import base64
import threading

from loguru import logger

logger.add("server.log", format="{time} {lever} {message}",
           level="DEBUG", rotation="1 MB", compression="zip")


@logger.catch
class Server:
    def __init__(self, ip: str, port: int):
        self.ip: str = ip
        self.port: int = port
        self.all_client: [] = []

        # Start listening for connection (Запускаем прослушивание соединений)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(0)
        threading.Thread(target=self.connect_handler).start()
        logger.info("Сервер запущен!")

    def connect_handler(self) -> None:
        while True:
            client, address = self.server.accept()
            if client not in self.all_client:
                self.all_client.append(client)
                threading.Thread(target=self.message_handler, args=(client,)).start()
                client.send('Успешное подключение к чату!'.encode('utf-8'))
            time.sleep(1)

    def message_handler(self, client_socket) -> None:
        while True:
            message = client_socket.recv(1024)
            print(message)

            # Delete the current socket (Удаляем текущий сокет)
            if message == b'exit':
                self.all_client.remove(client_socket)
                break

            for client in self.all_client:
                if client != client_socket:
                    client.send(message)
            time.sleep(1)

