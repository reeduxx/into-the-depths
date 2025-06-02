import socket
import threading
from TurnKeeper.TurnKeeper import TurnKeeper


class GameServer:
    def __init__(self, host=socket.gethostname(), port=55556, turn_time=3):
        self.host = host
        self.port = port
        self.turn_time = turn_time

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.clients = []
        self.nicknames = []
        self.turnkeeper = None
        self.lock = threading.Lock()

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message.encode('ascii'))
            except:
                continue

    def start_combat(self):
        with self.lock:
            if self.turnkeeper is None:
                print("[Server] Combat started!")
                self.turnkeeper = TurnKeeper(self.nicknames, self.turn_time)
                self.turnkeeper.register_event("turn_start", self.on_turn_start)
                self.turnkeeper.register_event("turn_end", self.on_turn_end)
                self.turnkeeper.enter_combat()

    def on_turn_start(self, player):
        self.broadcast(f"[TurnKeeper] It's {player}'s turn!")

    def on_turn_end(self, player):
        self.broadcast(f"[TurnKeeper] {player}'s turn ended.")

    def handle_client(self, client, nickname):
        while True:
            try:
                message = client.recv(1024).decode("ascii")
                print(f"[Received] {message}")

                if message.strip().lower() == "combat":
                    self.start_combat()
                else:
                    self.broadcast(f"{nickname}: {message}")

            except Exception as e:
                print(f"[Error] {e}")
                if client in self.clients:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    left_nickname = self.nicknames.pop(index)
                    self.broadcast(f"[Server] {left_nickname} left the game!")
                break

    def accept_connections(self):
        print(f"[Server] Listening on {self.host}:{self.port}...")
        while True:
            client, address = self.server_socket.accept()
            print(f"[Connection] {address} connected.")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')

            self.clients.append(client)
            self.nicknames.append(nickname)

            print(f"[Server] Nickname received: {nickname}")
            self.broadcast(f"[Server] {nickname} joined the game!")
            client.send('Connected to the server.'.encode('ascii'))

            thread = threading.Thread(target=self.handle_client, args=(client, nickname))
            thread.start()

    def start(self):
        self.accept_connections()


if __name__ == '__main__':
    server = GameServer()
    server.start()
