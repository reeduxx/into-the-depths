import threading
from TurnKeeper.TurnKeeper import TurnKeeper

class CombatManager:
    def __init__(self, players, turn_time, broadcast):
        self.players = players
        self.turn_time = turn_time
        self.broadcast = broadcast
        self.turn_keeper = TurnKeeper(players, turn_time)

        # Register turn events
        self.turn_keeper.register_event("turn_start", self.on_turn_start)
        self.turn_keeper.register_event("turn_end", self.on_turn_end)

    def start_combat(self):
        self.broadcast("Combat has started!\n".encode("ascii"))
        self.turn_keeper.enter_combat()

    def on_turn_start(self, player):
        self.broadcast(f"It's now {player}'s turn!\n".encode("ascii"))

    def on_turn_end(self, player):
        self.broadcast(f"{player}'s turn has ended.\n".encode("ascii"))

    def stop_combat(self):
        self.broadcast("Combat has ended!\n".encode("ascii"))
        self.turn_keeper.stop()