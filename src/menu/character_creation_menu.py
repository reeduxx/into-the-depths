import textwrap
from art.art import CREATE_ASCII
from player.character.species import Species
from util.json_loader import load_json
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
        self.species_data = load_json("player", "species.json")
        self.selected_species_index = 0
        self.name_complete = False
        self.species_class_complete = False
        self.stats_complete = False
    
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
    '''
    def display_species_class_input_box(self):
        species = self.species_list[self.selected_species_index]
        input_box_width = (self.term.width // 2) - 1
        padding = (input_box_width - len(species["name"]) - 2) // 2
        extra_padding = (input_box_width - len(species["name"]) - 2) % 2
        box_x = 1
        box_top_y = self.menu_start_y + 3
        box_bottom_y = self.term.height - 2
        box_color = self.term.darkgray if (self.species_class_complete or not self.name_complete) else self.term.normal
        
        with self.term.location(box_x, box_top_y):
            print(f"{box_color}╒{'═' * (input_box_width - 2)}╕")
        
        with self.term.location(box_x, box_top_y + 1):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_top_y + 2):
            print(f"{box_color}│{' ' * padding}{species["name"]}{' ' * (padding + extra_padding)}│")
        
        for y in range(box_top_y + 3, box_bottom_y - 1):
            with self.term.location(box_x, y):
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_bottom_y - 1):
            if not self.species_class_complete:
                print(f"{box_color}│{' ' * ((input_box_width - 38) // 2)}[←] Prev | [Enter] Select | [→] Next {' ' * ((input_box_width - 38) // 2)}│")
            else:
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_bottom_y):
            print(f"{box_color}╘{'═' * (input_box_width - 2)}╛")
    '''
    def display_species_class_input_box(self):
        species = Species(self.species_data[self.selected_species_index])
        input_box_width = (self.term.width // 2) - 1
        padding = (input_box_width - len(species.name) - 2) // 2
        extra_padding = (input_box_width - len(species.name) - 2) % 2
        box_x = 1
        box_top_y = self.menu_start_y + 3
        box_bottom_y = self.term.height - 2
        box_color = self.term.darkgray if (self.species_class_complete or not self.name_complete) else self.term.normal
        species_text = str(species).split('\n')

        with self.term.location(box_x, box_top_y):
            print(f"{box_color}╒{'═' * (input_box_width - 2)}╕")

        with self.term.location(box_x, box_top_y + 1):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")

        for i, line in enumerate(species_text):
            if box_top_y + 2 + i >= box_bottom_y - 2:
                break
            with self.term.location(box_x, box_top_y + 2 + i):
                if i == 0:
                    print(f"{box_color}│{' ' * padding}{self.term.underline}{line}{self.term.normal}{' ' * (padding + extra_padding)}│")
                else:
                    print(f"{box_color}│ {line}│")
            
        for y in range(box_top_y + 2 + len(species_text), box_bottom_y - 1):
            with self.term.location(box_x, y):
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")

        with self.term.location(box_x, box_bottom_y):
            print(f"{box_color}╘{'═' * (input_box_width - 2)}╛")

    def display_stats_input_box(self):
        input_box_width = (self.term.width // 2) - 2
        box_x = (self.term.width // 2) + 1
        box_top_y = self.menu_start_y + 3
        box_bottom_y = self.term.height - 2
        box_color = self.term.darkgray if (self.stats_complete or not self.species_class_complete) else self.term.normal
        
        with self.term.location(box_x, box_top_y):
            print(f"{box_color}╒{'═' * (input_box_width - 2)}╕")
        
        for y in range(box_top_y + 1, box_bottom_y):
            with self.term.location(box_x, y):
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_bottom_y):
            print(f"{box_color}╘{'═' * (input_box_width - 2)}╛")
    
    def handle_input(self):
        key = self.term.inkey(timeout=0.1)
        
        if not self.name_complete:
            if key.code == self.term.KEY_ENTER and len(self.name) > 0:
                self.name_complete = True
            elif key.code == self.term.KEY_BACKSPACE and len(self.name) > 0:
                self.name = self.name[:-1]
            elif key.isalnum() and len(self.name) < self.max_name_length:
                self.name += key
        elif not self.species_class_complete:
            if key.code == self.term.KEY_LEFT:
                self.selected_species_index = (self.selected_species_index - 1) % 4
            elif key.code == self.term.KEY_RIGHT:
                self.selected_species_index = (self.selected_species_index + 1) % 4
            elif key.code == self.term.KEY_ENTER:
                self.species_class_complete = True
        elif not self.stats_complete:
            if key.code == self.term.KEY_ENTER:
                self.stats_complete = True
                return False
        else:
            if key.code == self.term.KEY_ESCAPE:
                if self.stats_complete:
                    self.stats_complete = False
                elif self.species_class_complete:
                    self.species_class_complete = False
                elif self.name_complete:
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
                self.display_species_class_input_box()
                self.display_stats_input_box()
                
                if not self.handle_input():
                    break
        
        return self.name
    