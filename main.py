#!/usr/bin/python3.11
import random
import struct
import asyncio

from Board import Board
from View import display

# TCP Server

# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Semaphore, Thread

# 1 byte segments
BUF_SIZE = 1
HOST = ''
PORT = 12345
SHORT = 2


async def send_data(writer, data):
    """
    Send data to the client with a header and indication the data length.
    :param writer: The StreamWriter object for the client.
    :param data: The data to be sent.
    :return: The data from client.
    """
    header = struct.pack("!H", len(data))
    # sc.sendall(header + data)   # use for socket
    writer.write(header + data)
    await writer.drain()


class Game:
    """
    Main Game class that handles player connections and game logic.
    """

    def __init__(self):
        """
        Initialize the game board, players, and players id
        """
        self.board = Board(10, 5, 5, 10, 2)

        # Create player
        self.player1 = self.board.add_player("1", random.randint(0, self.board.n - 1),
                                             random.randint(0, self.board.n - 1))
        self.player2 = self.board.add_player("2", random.randint(0, self.board.n - 1),
                                             random.randint(0, self.board.n - 1))
        # self.lock = Semaphore()     # Semaphore for thread synchronization
        self.player_id = ['1', '2']  # List of player IDS

    async def hold_client(self, reader, writer):
        """
        Handle individual client connections and game interactions
        :param writer: The StreamWriter object for the client
        :param reader: The StreamReader object for the client
        :return: the play cmd and play id
        """
        # Use for threading:
        # with self.lock:
        #         player_id = self.player_id.pop(0).encode('utf-8')
        #         if player_id is None:
        #             self.send_data(sc, "FULL".encode('utf-8'))
        #             sc.close()
        #             return
        #         header = struct.pack("!H", len(player_id))
        #         sc.sendall(header)
        #         sc.sendall(struct.pack("B", int(player_id)))

        player_id = self.player_id.pop(0).encode('utf-8')
        if player_id is None:
            await send_data(writer, "FULL".encode('utf-8'))
            writer.close()
            await writer.wait_closed()
            return

        await send_data(writer, struct.pack("B", int(player_id)))

        try:
            while True:
                data = await reader.read(BUF_SIZE)

                if data == b'':
                    writer.close()
                    await writer.wait_closed()
                    break

                number = int.from_bytes(data, byteorder='big')

                player_input = None
                user_input = None

                # f0 is for direction, 0f is for player

                if number & 0x0f == 0x04:
                    player_input = '1'
                    print('Select Player 1')

                elif number & 0x0f == 0x08:
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

                elif number & 0xf0 == 0xf0:
                    user_input = 'G'

                if user_input == 'Q':
                    break

                if user_input is not None or player_input is not None or number & 0xf0 == 0xf0 or number & 0xf0 == 0xf4:
                    if number & 0xf0 == 0xf0:
                        display(self.board)
                    else:
                        try:
                            self.board.move_player(player_input, user_input)
                        except ValueError as details:
                            print(details)
                            # await send_data(writer, "ERROR".encode('uft-8'))

                    # always sending score and board state
                    sent_score = b''
                    for name, obj in self.board.players.items():
                        player_score = struct.pack('!H', int(obj['score']))
                        sent_score += player_score

                        print(f"Player {name} the score is {obj['score']}")

                    # await send_data(struct.pack('!H', len(sent_score + str(display(self.board)).encode('utf-8'))))
                    board_states = str(display(self.board)).encode('utf-8')
                    await send_data(writer, sent_score + board_states)
                    print(display(self.board))

        except ValueError as details:
            print(details)
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f'ERROR: {e}')
            writer.close()
            await writer.wait_closed()

    async def start(self):
        """
        Start the game server and listen for incoming client connections.
        """

        # Use for socket:
        # with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
        #     sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Details later
        #     sock.bind((HOST, PORT))  # Claim messages sent to port "PORT"
        #     sock.listen(2)  # Server only supports a single 3-way handshake at a time
        #     print('Server:', sock.getsockname())  # Server IP and port
        #       while True:
        #           sc, _ = sock.accept()  # Wait until a connection is established
        #           Thread(target=self.threads, args=(sc,)).start()     # Start a new thread for each client

        server = await asyncio.start_server(self.hold_client, HOST, PORT)
        address = server.sockets[0].getsockname()
        print(f'Server: {address}')

        await server.serve_forever()




if __name__ == "__main__":
    g = Game()
    # g.start()
    asyncio.run(g.start())
