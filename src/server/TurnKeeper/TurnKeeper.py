import time
import threading

class TurnKeeper:
    def __init__(self, players, turn_time):
        self.players = players
        self.turn_time = turn_time
        self.current_index = 0
        self.running = False
        self.event_listeners = {
            "turn_start": [],
            "turn_end": []
        }
        self.thread = None

    def register_event(self, event_name, callback):
        if event_name in self.event_listeners:
            self.event_listeners[event_name].append(callback)

    def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self.event_listeners:
            for callback in self.event_listeners[event_name]:
                callback(*args, **kwargs)

    def enter_combat(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def run(self):
        while self.running:
            current_player = self.players[self.current_index]
            self.trigger_event("turn_start", current_player)
            time.sleep(self.turn_time)
            self.trigger_event("turn_end", current_player)

            self.current_index = (self.current_index + 1) % len(self.players)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None