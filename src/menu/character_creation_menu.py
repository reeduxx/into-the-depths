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
    
    def display_title(self):
        opaque_color, translucent_color = get_colors(self.term)
        
        for line in CREATE_ASCII.splitlines():
            print(self.term.center(''.join(
            f"{opaque_color}{char}{self.term.normal}" if char in self.OPAQUE_BLOCKS else
            f"{translucent_color}{char}{self.term.normal}" if char in self.TRANSLUCENT_BLOCKS else
            char for char in line
        )))
    
    def display_menu(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            print(self.term.home + self.term.clear)
            self.display_title()
            input_box_width = self.max_name_length + 10
            box_x = (self.term.width - input_box_width) // 2
            box_y = self.menu_start_y - 2
            
            while True:
                with self.term.location(box_x, box_y):
                    print(f"╒{'═' * (input_box_width - 2)}╕")
                
                with self.term.location(box_x, box_y + 1):
                    print(f"│{' ' * (input_box_width - 2)}│")
                
                with self.term.location(box_x, box_y + 2):
                    print(f"│ Name: {self.name}{'_' * (self.max_name_length - len(self.name))} │")
                
                with self.term.location(box_x, box_y + 3):
                    print(f"│{' ' * (input_box_width - 2)}│")
                
                with self.term.location(box_x, box_y + 4):
                    print(f"╘{'═' * (input_box_width - 2)}╛")
                
                key = self.term.inkey()
                
                if key.code == self.term.KEY_ENTER and len(self.name) > 0:
                    break
                elif key.code == self.term.KEY_BACKSPACE and len(self.name) > 0:
                    self.name = self.name[:-1]
                elif key.isalnum() and len(self.name) < self.max_name_length:
                    self.name += key
        
        return self.name
    