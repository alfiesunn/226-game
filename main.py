#!/usr/bin/python3.11
import random
import struct

from Board import Board
from View import display

# TCP Server

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# 1 byte segments
BUF_SIZE = 1024
HOST = ''
PORT = 12345


class Game:
    # Setting size of board, and who many players
    def __init__(self):
        self.board = Board(10, 5, 5, 10, 2)

        # Create player
        self.player1 = self.board.add_player("1", random.randint(0, self.board.n - 1), random.randint(0, self.board.n - 1))
        self.player2 = self.board.add_player("2", random.randint(0, self.board.n - 1), random.randint(0, self.board.n - 1))

    def start(self):
        player_id = ['1','2']

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
                    print(data.decode('utf-8'))

                    if data.decode('utf-8') == 'id':
                        if len(player_id) > 0:
                            sc.send(player_id[0].encode('utf-8'))
                            player_id.pop(0)    # delete the player
                            print(player_id)
                        else:
                            sc.send('Error: 2 players are already exist.'.encode('utf-8'))
                    else:
                        # Convert the data to a bit string
                        number = int.from_bytes(data, byteorder='big')

                        player_input = None
                        user_input = None

                        sent_score = b''
                        for name, obj in self.board.players.items():
                            # print(f"Player {name} the score is {board.players[name]['score']}")
                            player_score = struct.pack('!H', int(obj['score']))
                            sent_score += player_score
                            print(f"Player {name} the score is {obj['score']}")
                        sc.sendall(sent_score)

                        # f0 is for direction, 0f is for player

                        if number & 0x0f == 0x04:
                            player_input = '1'
                            print('Select Player 1')

                        if number & 0x0f == 0x08:
                            player_input = '2'
                            print('Select Player 2')

                        if number & 0xf0 == 0x20:
                            user_input = 'U'
                            print(display(self.board))
                            print('Player Move Up')

                        elif number & 0xf0 == 0x40:
                            user_input = 'L'
                            print(display(self.board))
                            print('Player Move left')

                        elif number & 0xf0 == 0x60:
                            user_input = 'R'
                            print(display(self.board))
                            print('Player Move Right')

                        elif number & 0xf0 == 0x30:
                            user_input = 'D'
                            print(display(self.board))
                            print('Player Move Down')

                        elif number & 0xf0 == 0xf0:
                            user_input = 'G'
                            print(display(self.board))
                            sc.sendall(str(display(self.board)).encode('utf-8'))
                            print('Showing board')

                        elif number & 0xf0 == 0x80:
                            user_input = 'Q'
                            if user_input != 'Q':
                                pass
                            else:
                                print("Good Game My Friend!")
                                print('Player Quit')

                        if user_input is not None or player_input is not None or number & 0xf0 == 0xf0:
                            try:
                                self.board.move_player(player_input, user_input)
                            except ValueError as details:
                                print(details)
                        else:
                            print('Invalid input, disconnect right now.')
                            # sc.close()
                            break

                        # Send the result to the client




if __name__ == "__main__":
    g = Game()
    g.start()
# -----------------------------------------------------------------------------------------------------------------------------------
"""
Before Lab4 TCP
"""
        # while board.count_treasures():
        #     display(board)

            # playerInput = input('Which player do you want to move, 1 or 2\n')

            # userInput = input('(U)p (L)eft (R)ight (D)own (Q)uit?\n ').upper()

            # if userInput != 'Q':
            #     pass
            # else:
            #     print("Good Game My Friend!")
            #     exit()
            #
            # try:
            #     board.move_player(playerInput, userInput)
            # except ValueError as details:
            #     print(details)
            #
            # if not isinstance(userInput, str):
            #     raise TypeError("Error type.")
            #
            # for name, obj in board.players.items():
            #     # print(f"Player {name} the score is {board.players[name]['score']}")
            #     print(f"Player {name} the score is {obj['score']}")



