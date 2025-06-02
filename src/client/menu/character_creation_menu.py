from enum import Enum, auto
from client.menu.menu import Menu
from client.util import load_ascii_art

class CreationPhase(Enum):
    NAME = auto()
    SPECIES = auto()
    CLASS = auto()
    STATS = auto()
    COMPLETE = auto()

class CharacterCreationMenu(Menu):
    def __init__(self, term, config):
        super().__init__(term)
        self.config = config
        self.theme = self.config.get("theme", "auto")
        self.ascii_art = load_ascii_art("assets/ascii/create.txt")
        self.phase = CreationPhase.NAME
        self.max_name_length = 16
        self.name = ""
        self.name_confirmed = False
    
    def run(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            self.buffer.clear()

            while self.phase != CreationPhase.COMPLETE:
                if self.window_resized():
                    self._prev_width, self._prev_height = self.term.width, self.term.height
                    self.buffer.resize()
                    self.buffer.clear()
                
                self.display()
                self.buffer.render()
                key = self.term.inkey(timeout=0.1)
                self.handle_input(key)
            
            return self.name
    
    def display(self):
        opaque_color = self.term.white if self.theme == "dark" or self.theme == "auto" else self.term.black
        transparent_color = self.term.red if self.theme == "dark" or self.theme == "auto" else self.term.green
        self.draw_ascii_art(self.ascii_art, 1, opaque_color, transparent_color)
        self.display_name_input()
        self.display_species_input()
        self.display_class_input()
        self.display_stats_input()
    
    def handle_input(self, key):
        if self.phase == CreationPhase.NAME:
            self.handle_name_input(key)
    
    def display_name_input(self):
        box_width = self.max_name_length + 10
        box_x = (self.term.width - box_width) // 2
        box_y = 12
        self.draw_box(box_x, box_y, box_width, 4)
        name_display = "Name: " + self.name + ('_' if not self.name_confirmed else ' ') * (self.max_name_length - len(self.name))
        name_x = (self.term.width - len(name_display)) // 2
        name_y = box_y + 2
        self.buffer.draw_text(name_x, name_y, name_display)
    
    def display_species_input(self):
        box_width = (self.term.width - 1) // 2
        box_x = 1
        box_y = 17
        box_height = (self.term.height - 19) // 2
        self.draw_box(box_x, box_y, box_width, box_height)

    def display_class_input(self):
        box_width = (self.term.width - 1) // 2
        box_x = 1
        box_y = self.term.height - (self.term.height - 16) // 2
        box_height = (self.term.height - 20) // 2
        self.draw_box(box_x, box_y, box_width, box_height)
    
    def display_stats_input(self):
        box_width = (self.term.width - 1) // 2
        box_x = (self.term.width + 1) // 2
        box_y = 17
        box_height = self.term.height - 19
        self.draw_box(box_x, box_y, box_width, box_height)
    
    def handle_name_input(self, key):
        if key.code == self.term.KEY_ENTER and self.name:
            self.name_confirmed = True
            self.phase = CreationPhase.SPECIES
        elif key.code == self.term.KEY_BACKSPACE and self.name:
            self.name = self.name[:-1]
        elif (key.isalnum() or key.code == 32 or key == ' ') and len(self.name) < self.max_name_length:
            self.name += key