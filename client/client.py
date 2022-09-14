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


class Client(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ip = None
        self.port = None
        self.friend_public_key = None

        # Current client encryption keys (Ключи шифрования текущего клиента)
        self.my_public_key = None
        self.my_private_key = None

        # Check for the presence of the interlocutor ID (Проверка на наличие идентификатора собеседника)
        if len(os.listdir('friend_id')) == 0:
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_4.setEnabled(False)
            message = 'Поместите идентификатор собеседника в "friend_id"'
            self.ui.plainTextEdit.appendPlainText(message)

        # Checking if a personal ID has been created (Проверка, создан ли личный идентификатор)
        if not os.path.exists('private'):
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_4.setEnabled(False)
            message = 'Также необходимо сгенерировать свой идентификатор'
            self.ui.plainTextEdit.appendPlainText(message)

        else:
            # Uploading current client data (Подгрузка данных текущего клиента)
            with shelve.open('private') as file:
                self.my_public_key = file['pubkey']
                self.my_private_key = file['privkey']
                self.ip = file['ip']
                self.port = file['port']

