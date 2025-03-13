from art.art import CREATE_ASCII
from util.util import get_colors

class CharacterCreationMenu:
    OPAQUE_BLOCKS = {'█', '▌', '▀', '▄'}
    TRANSLUCENT_BLOCKS = {'▓', '▒', '░'}
    
    def __init__(self, term):
        self.term = term
        self.max_name_length = 16
        self.selected_index = 0
        self.name = ""
        self.menu_start_y = 14
        self.name_complete = False
    
    def display_title(self):
        opaque_color, translucent_color = get_colors(self.term)
        print(self.term.home + self.term.clear)
        
        for line in CREATE_ASCII.splitlines():
            print(self.term.center(''.join(
            f"{opaque_color}{char}{self.term.normal}" if char in self.OPAQUE_BLOCKS else
            f"{translucent_color}{char}{self.term.normal}" if char in self.TRANSLUCENT_BLOCKS else
            char for char in line
        )))
    
    def display_name_input_box(self):
        input_box_width = self.max_name_length + 10
        box_x = (self.term.width - input_box_width) // 2
        box_y = self.menu_start_y - 2
        box_color = self.term.darkgray if self.name_complete else self.term.normal
        
        with self.term.location(box_x, box_y):
            print(f"{box_color}╒{'═' * (input_box_width - 2)}╕")
        
        with self.term.location(box_x, box_y + 1):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_y + 2):
            if not self.name_complete:
                print(f"{box_color}│ Name: {self.name}{'_' * (self.max_name_length - len(self.name))} │")
            else:
                print(f"{box_color}│ Name: {self.name}{' ' * (self.max_name_length - len(self.name))} │")
        
        with self.term.location(box_x, box_y + 3):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_y + 4):
            print(f"{box_color}╘{'═' * (input_box_width - 2)}╛")
    
    def handle_input(self):
        key = self.term.inkey(timeout=0.1)
        
        if not self.name_complete:
            if key.code == self.term.KEY_ENTER and len(self.name) > 0:
                self.name_complete = True
                return False
            elif key.code == self.term.KEY_BACKSPACE and len(self.name) > 0:
                self.name = self.name[:-1]
            elif key.isalnum() and len(self.name) < self.max_name_length:
                self.name += key
        else:
            if key.code == self.term.KEY_ESCAPE:
                self.name_complete = False
        
        return True
    
    def get_input(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            prev_width, prev_height = self.term.width, self.term.height
            self.display_title()
            
            while True:
                if self.term.width != prev_width or self.term.height != prev_height:
                    prev_width, prev_height = self.term.width, self.term.height
                    self.display_title()
                    
                self.display_name_input_box()
                
                if not self.handle_input():
                    break
        
        return self.name
    