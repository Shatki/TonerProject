# -*- coding: utf-8 -*-
from socket import *

HOST = 'localhost'
PORT = 21567
BUF_SIZE = 1024  # Потом пересмотреть
ADDR = (HOST, PORT)


def send_data(data):
    if data:
        tcpClntSock = socket(AF_INET, SOCK_STREAM)
        tcpClntSock.connect(ADDR)
        tcpClntSock.send(data.encode())
        return tcpClntSock.recv(BUF_SIZE).decode()
    else:
        return False

# print(send_data("Hello!"))

# print(send_data("stop"))
