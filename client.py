#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM
from threading import Semaphore, Thread

import struct

SHORT = 2
BUF_SIZE = 1
HOST = '127.0.0.1'
PORT = 12345

UP = 0b00100000
LEFT = 0b01000000
RIGHT = 0b01100000
DOWN = 0b00110000
QUIT = 0b10000000
GET = 0b11110000

PLAYER1 = 0b0100
PLAYER2 = 0b1000


def receive_data(sc, size):
    """
    Utility function to receive data from the socket until the desired size is reached.
    :param sc: From the server side
    :param size: data size from server
    :return: data from server
    """
    data = b''
    while len(data) < size:
        curr_data = sc.recv(size - len(data))
        if curr_data == b'':
            return data
        data += curr_data
    return data


def receive_size_and_data(sock):
    """

    :param sock:
    :return:
    """
    header = receive_data(sock, SHORT)
    data_size = struct.unpack("!H", header)[0]
    return receive_data(sock, data_size), data_size


def print_scores_and_board(data):
    """

    :param data:
    :return:
    """
    player1_score, player2_score = struct.unpack('!HH', data[:4])
    print(f'Player 1 Score: {player1_score}')
    print(f'Player 2 Score: {player2_score}')
    print()
    board = data[4:].decode('utf-8')
    print(board)


def send_cmd(sock, player_id, cmd):
    """

    :param sock:
    :param player_id:
    :param cmd:
    :return:
    """
    pack_data = player_id | cmd
    pack_cmd = struct.pack('!B', pack_data)
    sock.sendall(pack_cmd)


def main():
    """
    Main function to handle client operations
    :return: Player score and Game board
    """
    with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
        sock.connect((HOST, PORT))  # Initiates 3-way handshake
        print('Client:', sock.getsockname())  # Client IP and port

        # Receive the size of the player id from server
        player_id_size = struct.unpack("!H", receive_data(sock, SHORT))[0]
        # Receive the player id
        player_id = int.from_bytes(sock.recv(player_id_size), byteorder="big")

        if player_id == 'FULL':
            print('Error: 2 players are already exist.')
            exit()

        if player_id == 0x01:
            print(f'Connecting as Player {player_id}')
            print()
            player_id = PLAYER1
        elif player_id == 0x02:
            print(f'Connecting as Player {player_id}')
            print()
            player_id = PLAYER2

        while True:
            send_cmd(sock, player_id, GET)
            data, data_size = receive_size_and_data(sock)

            # Output the board and scores
            if data_size > 4:
                print_scores_and_board(data)

            # Prompt the user input
            message = input('(U)p (L)eft (R)ight (D)own (Q)uit?\n').upper()

            if message == 'Q':
                cmd = QUIT
                print('Good Bye!')
                send_cmd(sock, player_id, cmd)
                break
            elif message == 'U':
                cmd = UP
            elif message == 'L':
                cmd = LEFT
            elif message == 'R':
                cmd = RIGHT
            elif message == 'D':
                cmd = DOWN
            else:
                print('Invalid Input, Enter again.')
                continue

            if message in ['U', 'L', 'R', 'D']:
                # pack the cmd and sent to server
                send_cmd(sock, player_id, cmd)
                # print(data)
                data, data_size = receive_size_and_data(sock)
                # Output the board and scores
                if data_size > 4:
                    print_scores_and_board(data)


if __name__ == "__main__":
    main()
