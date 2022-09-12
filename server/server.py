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
