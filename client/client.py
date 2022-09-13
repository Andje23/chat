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