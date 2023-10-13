#!/usr/bin/python3.11
import random

from Board import Board
from View import display

# TCP Server

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# 1 byte segments
BUF_SIZE = 1
HOST = '127.0.0.1'
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Details later
    sock.bind((HOST, PORT))  # Claim messages sent to port "PORT"
    sock.listen(1)  # Server only supports a single 3-way handshake at a time
    print('Server:', sock.getsockname())  # Server IP and port
    while True:
        sc, _ = sock.accept()  # Wait until a connection is established
        with sc:
            # Receive the input from the client
            data = sc.recv(BUF_SIZE)

            # Convert the data to a bit string
            number = int.from_bytes(data, byteorder='big')
            bit_string = '{0:b}'.format(number)
            print(bit_string)

            # Figure out which bits are set
            for p in range(8):
                print(f'Bit {p} is {1 if number & 2 ** p > 0 else 0}')

            # Figure out if all four top bits are set
            if number & 0xf0 == 0xf0:
                print('All four top bits are set')

            # Send the result to the client
            sc.sendall(b'You sent: ' + bit_string.encode() + b'\n')

# Setting size of board, and who many players
board = Board(10, 5, 5, 10, 2)

# Create player
board.add_player("1", random.randint(0, board.n - 1), random.randint(0, board.n - 1))
board.add_player("2", random.randint(0, board.n - 1), random.randint(0, board.n - 1))

# while board.count_treasures():
while True:
    display(board)

    playerInput = input('Which player do you want to move, 1 or 2\n')

    userInput = input('(U)p (L)eft (R)ight (D)own (Q)uit?\n ').upper()

    if userInput != 'Q':
        pass
    else:
        print("Good Game My Friend!")
        exit()

    try:
        board.move_player(playerInput, userInput)
    except ValueError as details:
        print(details)

    if not isinstance(userInput, str):
        raise TypeError("Error type.")

    for name, obj in board.players.items():
        # print(f"Player {name} the score is {board.players[name]['score']}")
        print(f"Player {name} the score is {obj['score']}")



