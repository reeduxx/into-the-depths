import socket 
import threading
from typing import Optional, Dict
import pickle
from common.player.character import Character
from server import GamePhase

class Client:
    def __init__(self, ip, character: Character):
        self.character = character
        self.socket: Optional[socket.socket]= None
        self.connected = False
        self.running = False

        self.current_phase = GamePhase.LOBBY
        self.position = (0,0)
        self.in_combat = False

        self.receive_thread: Optional[threading.Thread] = None
        self.message_queue = []
        self.queue_lock = threading.Lock()

    def connect_to_server(self, host: str = socket.gethostname(), port: int = 55556) -> bool:

        #attempts server connection and sends clients character data as a handshake. Returns T/F.

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host,port))

            handshake_data = {
                'type': 'character_join',
                'character_data': self.character.serialize(),
                'player_name': self.character.name
            }
            self.send_message(handshake_data)

            self.connected = True 
            self.running = True

            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()

            return True
        
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
        

    def send_message(self, message_data: Dict):
        #Send message to server. expects Dict formatting

        if not self.connected:
            return False
        
        try:
            pickled_message = pickle.dumps(message_data)
            if self.socket != None:
                self.socket.sendall(pickled_message)

        except Exception as e:
            print(f"Failed to send message: {e}")
            return False


    def receive_messages(self):
        # messages from server in separate thread
        while self.running:
            try:
                if self.socket != None:# Receive message length
                    length_bytes = self.socket.recv(4)
                    if not length_bytes:
                        break
                    
                    message_length = int.from_bytes(length_bytes, 'big')
                    
                    # Receive full message
                    message_data = b''
                    while len(message_data) < message_length:
                        chunk = self.socket.recv(message_length - len(message_data))
                        if not chunk:
                            break
                        message_data += chunk
                    
                    # Deserialize and queue message
                    message = pickle.loads(message_data)
                    with self.queue_lock:
                        self.message_queue.append(message)
                    
            except Exception as e:
                if self.running:
                    print(f"Error receiving message: {e}")
                break


