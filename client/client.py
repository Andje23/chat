import os
import sys
import rsa
import time
import shelve
import socket
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from des import *


# Monitoring of incoming message (Мониторинг входящих сообщений)
class MessageMonitor(QtCore.QThread):
    my_signal = QtCore.pyqtSignal(str)

    def __init__(self, server_socket: socket.socket, private_key: int, parent=None) -> None:
        QtCore.QThread.__init__(self, parent)
        self.server_socket: socket.socket = server_socket
        self.private_key: int = private_key
        self.message: str = None

    def run(self) -> None:
        while True:
            try: # Data from the interlocutor (encrypted) Данные от собеседника (зашифрованные)
                self.message = self.server_socket.recv(1024)
                decrypt_message = rsa.decrypt(self.message, self.private_key)
                self.my_signal.emit(decrypt_message.decode('utf-8'))
            except:  # Data from the server (not encrypted) Данные от сервера (не зашрованные)
                self.my_signal.emit(self.message.decode('utf-8'))