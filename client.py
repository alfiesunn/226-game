#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 65432

with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
    sock.connect((HOST, PORT))   # Initiates 3-way handshake
    print('Client:', sock.getsockname())  # Client IP and port




