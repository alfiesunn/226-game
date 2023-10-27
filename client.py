#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import struct


BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
CMD_MASK = 0b11110000
UP = 0b00100000
LEFT = 0b01000000
RIGHT = 0b01100000
DOWN = 0b00110000
QUIT = 0b10000000
GET = 0b11110000

PLAYER_MASK = 0b00001100
PLAYER1 = 0b0100
PLAYER2 = 0b1000
PLAYER1_NAME = '1'
PLAYER2_NAME = '2'

ERROR = b'E'
OK = b'O'


with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
    sock.connect((HOST, PORT))   # Initiates 3-way handshake
    print('Client:', sock.getsockname())  # Client IP and port
# s = socket(AF_INET, SOCK_STREAM)
# s.connect((HOST, PORT))
# print('Client:', s.getsockname())  # Client IP and port

def start_client():
    sock.sendall('id'.encode('utf-8'))
    data_size = sock.recv(BUF_SIZE)
    player_id = data_size.decode('utf-8')
    print(player_id)

    if player_id == 'Error: 2 players are already exist.':
        quit()


def main():
    start_client()
    while True:
        message = input('(U)p (L)eft (R)ight (D)own (Q)uit?\n').upper()
        if message == 'Q':
            sock.sendall(struct.pack('!H', QUIT))
            quit()
        elif message == 'U':
            sock.sendall(struct.pack('!H', UP))
        elif message == 'L':
            sock.sendall(struct.pack('!H', LEFT))
        elif message == 'R':
            sock.sendall(struct.pack('!H', RIGHT))
        elif message == 'D':
            sock.sendall(struct.pack('!H', DOWN))
        else:
            print('Invalid Input, Enter again.')


if __name__ == "__main__":
    main()




