from art.art import CREATE_ASCII
from menu.menu import Menu
from player.character.class_generator import ClassGenerator
from player.character.species_generator import SpeciesGenerator
from player.character.stats_generator import StatsGenerator
from util.json_loader import load_json

class CharacterCreationMenu(Menu):
    stat_names = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

    def __init__(self, term):
        super().__init__(term)
        self.max_name_length = 16
        self.name = ""
        self.menu_start_y = 14
        self.species_data = load_json("player", "species.json")
        self.species_generator = SpeciesGenerator(self.species_data)
        self.selected_species_index = 0
        self.selected_species = self.species_generator.generate(self.selected_species_index)
        self.class_data = load_json("player", "classes.json")
        self.class_generator = ClassGenerator(self.class_data)
        self.selected_class_index = 0
        self.selected_class = self.class_generator.generate(self.selected_class_index)
        self.stats_generator = StatsGenerator(self.class_data)
        self.stats = self.stats_generator.generate(self.selected_class_index)
        self.invested_stats = [0] * len(self.stats)
        self.selected_stat_index = 0
        self.investment_points = 5
        self.name_complete = False
        self.species_complete = False
        self.class_complete = False
        self.stats_complete = False

    def update_species(self):
        self.selected_species = self.species_generator.generate(self.selected_species_index)

    def update_class(self):
        self.selected_class = self.class_generator.generate(self.selected_class_index)
        self.stats = self.stats_generator.generate(self.selected_class_index)

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
                print(
                    f"{box_color}│ Name: {self.name}{'_' * (self.max_name_length - len(self.name))} │"
                )
            else:
                print(
                    f"{box_color}│ Name: {self.name}{' ' * (self.max_name_length - len(self.name))} │"
                )

        with self.term.location(box_x, box_y + 3):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")

        with self.term.location(box_x, box_y + 4):
            print(f"{box_color}╘{'═' * (input_box_width - 2)}╛")

    def display_species_class_input_box(self, selection, is_complete, is_previous_complete):
        """
        Builds and prints a selection menu box for either species or class.
        
        Parameters:
        - selection: The selected species or class object.
        - is_complete: Boolean indicating if the current selection is finalized.
        - is_previous_complete: Boolean indicating if the previous step is complete.
        """
        input_box_width = (self.term.width // 2) - 1
        input_box_height = (self.term.height - self.menu_start_y - 5) // 2
        padding = (input_box_width - len(selection.name) - 2) // 2
        extra_padding = (input_box_width - len(selection.name) - 2) % 2
        box_x = 1

        # Determine box position (species goes on top, class below it)
        if selection == self.selected_species:
            box_top_y = self.menu_start_y + 3
        else:
            box_top_y = self.menu_start_y + input_box_height + 3

        box_bottom_y = box_top_y + input_box_height - 1
        box_color = self.term.darkgray if (is_complete or not is_previous_complete) else self.term.normal
        selection_text = str(selection.__str__(input_box_width - 4)).split('\n')

        with self.term.location(box_x, box_top_y):
            print(f"{box_color}╒{'═' * (input_box_width - 2)}╕")

        with self.term.location(box_x, box_top_y + 1):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")

        for i, line in enumerate(selection_text):
            if box_top_y + 2 + i >= box_bottom_y - 2:
                break
            with self.term.location(box_x, box_top_y + 2 + i):
                if i == 0:
                    print(f"{box_color}│{' ' * padding}{self.term.underline}{line}{self.term.normal}{' ' * (padding + extra_padding)}{box_color}│")
                else:
                    padding = input_box_width - len(line) - 3
                    print(f"{box_color}│ {line}{' ' * padding}│")

        for y in range(box_top_y + 2 + len(selection_text), box_bottom_y - 2):
            with self.term.location(box_x, y):
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")

        with self.term.location(box_x, box_bottom_y - 2):
            if not is_complete and is_previous_complete:
                print(f"{box_color}│{' ' * ((input_box_width - 51) // 2)}[←] Prev | [ESC] Back | [Enter] Select | [→] Next {' ' * (((input_box_width - 51) // 2) - 1)}│")
            else:
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")

        with self.term.location(box_x, box_bottom_y - 1):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")

        with self.term.location(box_x, box_bottom_y):
            print(f"{box_color}╘{'═' * (input_box_width - 2)}╛")

    def display_stats_input_box(self):
        """
        Builds and prints the stats menu box
        """
        input_box_width = (self.term.width // 2) - 2
        box_x = (self.term.width // 2) + 1
        box_top_y = self.menu_start_y + 3
        box_bottom_y = self.term.height - 2
        box_color = self.term.darkgray if (self.stats_complete or not self.class_complete) else self.term.normal

        with self.term.location(box_x, box_top_y):
            print(f"{box_color}╒{'═' * (input_box_width - 2)}╕")
        
        with self.term.location(box_x, box_top_y + 1):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")

        with self.term.location(box_x, box_top_y + 2):
            padding = (input_box_width - 2) // 2 - 2
            print(f"{box_color}│{' ' * padding}{self.term.underline}Stats{self.term.normal}{' ' * (padding - 1)}│")

        for y, stat in enumerate(self.stat_names):
            with self.term.location(box_x, box_top_y + y + 3):
                padding = (input_box_width - 9) // 2
                if y == self.selected_stat_index and self.class_complete:
                    print(f"{box_color}│ {' ' * padding}{stat}: {self.term.reverse}{(self.stats[y] + self.invested_stats[y]):2}{self.term.normal}{box_color}{' ' * padding}│")
                else:
                    print(f"{box_color}│ {' ' * padding}{stat}: {(self.stats[y] + self.invested_stats[y]):2}{' ' * padding}│")

        for y in range(box_top_y + len(self.stats) + 3, box_bottom_y - 4):
            with self.term.location(box_x, y):
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_bottom_y - 4):
            if not self.stats_complete and self.class_complete:
                print(f"{box_color}│{' ' * ((input_box_width - 22) // 2)}Investment Points: {self.investment_points:2}{' ' * (((input_box_width - 22) // 2) - 1)}│")
            else:
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_bottom_y - 3):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_bottom_y - 2):
            if not self.stats_complete and self.class_complete:
                print(f"{box_color}│{' ' * ((input_box_width - 52) // 2)}[←] Add | [ESC] Back | [Enter] Finish | [→] Remove {' ' * (((input_box_width - 52) // 2) - 1)}│")
            else:
                print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_bottom_y - 1):
            print(f"{box_color}│{' ' * (input_box_width - 2)}│")
        
        with self.term.location(box_x, box_bottom_y):
            print(f"{box_color}╘{'═' * (input_box_width - 2)}╛")
    
    def combine_stats(self):
        for i, stat in enumerate(self.invested_stats):
            self.stats[i] += stat
    
    def handle_input(self):
        """
        Reads the player input and updates the current menu
        
        Returns:
            Whether the player has finished completing their character
        """
        key_map = {
            self.term.KEY_UP: lambda: setattr(self, 'selected_stat_index', (self.selected_stat_index - 1) % len(self.stat_names)),
            self.term.KEY_DOWN: lambda: setattr(self, 'selected_stat_index', (self.selected_stat_index + 1) % len(self.stat_names))
        }
        
        key = self.term.inkey(timeout=0.1)

        if key.code == self.term.KEY_ESCAPE:
            if self.stats_complete:
                self.stats_complete = False
            elif self.class_complete:
                self.class_complete = False
            elif self.species_complete:
                self.species_complete = False
            elif self.name_complete:
                self.name_complete = False
        if not self.name_complete:
            if key.code == self.term.KEY_ENTER and len(self.name) > 0:
                self.name_complete = True
            elif key.code == self.term.KEY_BACKSPACE and len(self.name) > 0:
                self.name = self.name[:-1]
            elif key.isalnum() and len(self.name) < self.max_name_length:
                self.name += key
        elif not self.species_complete:
            if key.code == self.term.KEY_LEFT:
                self.selected_species_index = (self.selected_species_index - 1) % len(self.species_data)
                self.update_species()
            elif key.code == self.term.KEY_RIGHT:
                self.selected_species_index = (self.selected_species_index + 1) % len(self.species_data)
                self.update_species()
            elif key.code == self.term.KEY_ENTER:
                self.species_complete = True
        elif not self.class_complete:
            if key.code == self.term.KEY_LEFT:
                self.selected_class_index = (self.selected_class_index - 1) % len(self.class_data)
                self.update_class()
            elif key.code == self.term.KEY_RIGHT:
                self.selected_class_index = (self.selected_class_index + 1) % len(self.class_data)
                self.update_class()
            elif key.code == self.term.KEY_ENTER:
                self.class_complete = True
        elif not self.stats_complete:
            if key.code in key_map:
                key_map[key.code]()
            elif key.code == self.term.KEY_LEFT:
                if self.invested_stats[self.selected_stat_index] > 0:
                    self.invested_stats[self.selected_stat_index] -= 1
                    self.investment_points += 1
            elif key.code == self.term.KEY_RIGHT:
                if self.investment_points > 0:
                    self.invested_stats[self.selected_stat_index] += 1
                    self.investment_points -= 1
            elif key.code == self.term.KEY_ENTER:
                if self.investment_points == 0:
                    self.stats_complete = True
                    self.combine_stats()
                    return False

        return True

    def get_input(self):
        """
        Handles the loop that displays/updates the title and menu boxes
        
        Returns:
            Player name, species, class, and stats
        """
        with self.term.cbreak(), self.term.hidden_cursor():
            prev_width, prev_height = self.term.width, self.term.height
            self.display_title(CREATE_ASCII, version=False)

            while True:
                if self.term.width != prev_width or self.term.height != prev_height:
                    prev_width, prev_height = self.term.width, self.term.height
                    self.display_title(CREATE_ASCII, version=False)

                self.display_name_input_box()
                self.display_species_class_input_box(self.selected_species, self.species_complete, self.name_complete)
                self.display_species_class_input_box(self.selected_class, self.class_complete, self.species_complete)
                self.display_stats_input_box()

                if not self.handle_input():
                    break

        return self.name, self.selected_species, self.selected_class, self.stats
