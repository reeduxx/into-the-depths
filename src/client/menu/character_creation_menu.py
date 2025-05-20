from enum import Enum, auto
from client.menu.menu import Menu
from client.util import load_config

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
        if self.phase == CreationPhase.NAME:
            self.display_name_input()
    
    def handle_input(self, key):
        if self.phase == CreationPhase.NAME:
            self.handle_name_input(key)
    
    def display_name_input(self):
        box_width = self.max_name_length + 10
        box_x = (self.term.width - box_width) // 2
        box_y = self.term.height // 3
        self.draw_box(box_x, box_y, box_width, 5)
        label = "Enter Name: "
        self.center_text(box_y - 2, label, style=self.term.bold)
        name_display = self.name + ('_' if not self.name_confirmed else '')
        name_x = (self.term.width - len(name_display)) // 2
        name_y = box_y + 2
        self.buffer.draw_text(name_x, name_y, name_display, style=self.term.green)
    
    def handle_name_input(self, key):
        if key.code == self.term.KEY_ENTER and self.name:
            self.name_confirmed = True
            self.phase = CreationPhase.SPECIES
        elif key.code == self.term.KEY_BACKSPACE and self.name:
            self.name = self.name[:-1]
        elif key.isalnum() and len(self.name) < self.max_name_length:
            self.name += key
        elif key.code == self.term.KEY_ESCAPE:
            self.name = ""