#!/usr/bin/python3.11
import random
import struct

from Board import Board
from View import display

# TCP Server

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Semaphore, Thread

# 1 byte segments
BUF_SIZE = 1
HOST = ''
PORT = 12345
SHORT = 2


class Game:
    # Setting size of board, and who many players
    def __init__(self):
        self.board = Board(10, 5, 5, 10, 2)

        # Create player
        self.player1 = self.board.add_player("1", random.randint(0, self.board.n - 1), random.randint(0, self.board.n - 1))
        self.player2 = self.board.add_player("2", random.randint(0, self.board.n - 1), random.randint(0, self.board.n - 1))
        self.lock = Semaphore()
        self.player_id = ['1', '2']

    def send_data(self, sc, data):
        """
        Pack the data and sent all
        :param sc: The socket object for client
        :param data: The data the
        :return:
        """
        header = struct.pack("!H", len(data))
        sc.sendall(header + data)

    def threads(self, sc):
        with self.lock:
                player_id = self.player_id.pop(0).encode('utf-8')

                if player_id is None:
                    self.send_data(sc, "FULL".encode('utf-8'))
                    sc.close()
                    return
                header = struct.pack("!H", len(player_id))
                sc.sendall(header)

                sc.sendall(struct.pack("B", int(player_id)))

        try:
            while True:
                data = sc.recv(BUF_SIZE)

                number = int.from_bytes(data, byteorder='big')

                player_input = None
                user_input = None

                # f0 is for direction, 0f is for player

                if number & 0x0f == 0x04:
                    player_input = '1'
                    print('Select Player 1')

                if number & 0x0f == 0x08:
                    player_input = '2'
                    print('Select Player 2')

                if number & 0xf0 == 0x20:
                    user_input = 'U'
                    print('Player Move Up')

                elif number & 0xf0 == 0x40:
                    user_input = 'L'
                    print('Player Move left')

                elif number & 0xf0 == 0x60:
                    user_input = 'R'
                    print('Player Move Right')

                elif number & 0xf0 == 0x30:
                    user_input = 'D'
                    print('Player Move Down')

                elif number & 0xf0 == 0x80:
                    user_input = 'Q'
                    print('Player Chose Quite')

                if user_input == 'Q':
                    sc.close()
                    return

                with self.lock:
                    if user_input is not None or player_input is not None or number & 0xf0 == 0xf0:
                        try:
                            self.board.move_player(player_input, user_input)
                        except ValueError as details:
                            print(details)
                    else:
                        print('Invalid input, disconnect right now.')
                        # sc.close()

                    # always sending score and board state
                    sent_score = b''
                    for name, obj in self.board.players.items():
                        player_score = struct.pack('!H', int(obj['score']))
                        sent_score += player_score

                        print(f"Player {name} the score is {obj['score']}")
                    sc.sendall(struct.pack('!H', len(sent_score + str(display(self.board)).encode('utf-8'))))
                    sc.sendall(sent_score)
                    # print(sent_score)
                    sc.sendall(str(display(self.board)).encode('utf-8'))
                    print(display(self.board))

        except ValueError as details:
            print(details)
        except Exception as e:
            print(f'ERROR: {e}')

    def start(self):
        with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Details later
            sock.bind((HOST, PORT))  # Claim messages sent to port "PORT"
            sock.listen(2)  # Server only supports a single 3-way handshake at a time
            print('Server:', sock.getsockname())  # Server IP and port

            while True:
                sc, _ = sock.accept()  # Wait until a connection is established
                Thread(target=self.threads, args=(sc,)).start()


if __name__ == "__main__":
    g = Game()
    g.start()
# ----------------------------------------------------------------------------------------------------------------------------------