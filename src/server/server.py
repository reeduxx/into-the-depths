import socket
import threading
from TurnKeeper.TurnKeeper import TurnKeeper
from gamephase import GamePhase
import pickle


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
        self.game_phase = GamePhase.LOBBY
        self.lock = threading.Lock()

        #helps route and build commands for the server
        self.action_router = {
        "atk": self.handle_attack,
        "itm": self.handle_item_use,
        "mov": self.handle_move,
        }

    def handle_attack(self, player_name, data):
        try:
            target, attacktype = data.split(":")
            print(f"[Combat] {player_name} attacks {target} using {attacktype}!")
            #TODO apply actual combat logic
        except  ValueError:
            print(f"[ERROR] invalid attack from {player_name}: {data}")

        print(f"[ITEM] {player_name} uses item: {data}")
    def handle_item_use(self, player_name, data):
        #TODO apply item effects here to player data.

    def handle_move(self, player_name, data):
        pass

    def parse_message(self, message):
        try:
            header, data = message.split("]", 1)
            header = header.strip("[")
            name, actioncode = [x.strip() for x in header.split(",")]
            data = data.strip()
            return name,actioncode,data
        except ValueError:
            print("Invalid message format!")
            return None, None, None

    def broadcast(self, message_dict):
        for client in self.clients:
            try:
                client.send_to_client(client, message_dict)
            except:
                continue

    def switch_state(self, game_state):

        """Planned future usage when switching phases:
       current_phase = GamePhase.LOBBY
       self.switch_state(current_state)
        """
        
        match game_state:
            case GamePhase.LOBBY:
                return "Game lobby code here"
            case GamePhase.COMBAT:
                return "Combat code here"
            case GamePhase.EXPLORATION:
                return "Exploration code here"
            case _:
                return "Unknown game state"


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

    def send_to_client(self, client, message_dict):
        try:
            pickled = pickle.dumps(message_dict)
            length = len(pickled).to_bytes(4, byteorder='big')
            client.sendall(length + pickled)
        except Exception as e:
            print(f"[Warning] Failed to send message: {e}")

    def handle_client(self, client, nickname):
        while True:
            try:
                # Step 1: Read 4-byte message length
                length_bytes = client.recv(4)
                if not length_bytes:
                    raise ConnectionResetError("Client disconnected.")

                message_length = int.from_bytes(length_bytes, byteorder='big')

                # Step 2: Read full message of known length
                message_data = b''
                while len(message_data) < message_length:
                    chunk = client.recv(message_length - len(message_data))
                    if not chunk:
                        raise ConnectionResetError("Client disconnected mid-message.")
                    message_data += chunk

                # Step 3: Deserialize (unpickle) message
                message = pickle.loads(message_data)
                print(f"[Received] {nickname}: {message}")

                # Step 4: Route message based on type
                message_type = message.get("type")
                if message_type == "character_join":
                    # Handle player join handshake
                    self.register_player(nickname, message)
                elif message_type == "action":
                    name = message.get("player_name")
                    actioncode = message.get("actioncode")
                    data = message.get("data")

                    if actioncode in self.action_router:
                        self.action_router[actioncode](name, data)
                    else:
                        self.send_to_client(client, {"type": "error", "msg": f"Unknown action: {actioncode}"})
                else:
                    self.send_to_client(client, {"type": "error", "msg": f"Unknown message type: {message_type}"})

            except Exception as e:
                print(f"[Error] {nickname}: {e}")
                if client in self.clients:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    left_nickname = self.nicknames.pop(index)
                    self.broadcast({"type": "info", "msg": f"{left_nickname} left the game."})
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
