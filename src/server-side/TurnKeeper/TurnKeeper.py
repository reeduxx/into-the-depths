import threading

#will take in a list of players to help keep track of their turns
class TurnKeeper:

    def __init__(self, players, turn_time):
        self.players = players
        self.index = 0
        #small initial timer value so I can test it
        self.turn_time = turn_time
        
    #!might have to refactor later to just be called with no params. Passing it a name for now to test with!
    #takes a username and compares it to the index of players at self.index
    def is_turn(self, username):
        return True if self.players[self.index] == username else False

    #iterates to next player, doesnt roll over list size
    def next_player(self):
        if (self.index + 1) < (len(self.players)):
            self.index += 1
        else:
            self.index = 0
    
    def start_turn_timer(self):
        timer = threading.Timer(self.turn_time,  self.next_player)
        timer.start()


            
            

