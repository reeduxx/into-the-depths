from client.menu.menu import Menu

class MainMenu(Menu):
    MENU_OPTIONS = ["Continue", "New Game", "Credits", "Exit"]

    def __init__(self, term):
        super().__init__(term)
        self.selected_index = 0
        self.menu_width = max(len(opt) for opt in self.MENU_OPTIONS) + 6
        self.menu_height = len(self.MENU_OPTIONS) * 2 + 2
    
    def run(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                if self.window_resized():
                    self._prev_width, self._prev_height = self.term.width, self.term.height
                    self.clear_screen()
                
                self.display_menu()
                key = self.term.inkey(timeout=0.1)
                
                if key.code == self.term.KEY_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.MENU_OPTIONS)
                elif key.code == self.term.KEY_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.MENU_OPTIONS)
                elif key.code == self.term.KEY_ENTER:
                    return self.MENU_OPTIONS[self.selected_index].lower().replace(' ', '_')
    
    def display_menu(self):
        x = (self.term.width - self.menu_width) // 2
        y = max(14, (self.term.height - self.menu_height) // 2)
        self.draw_box(x, y, self.menu_width, self.menu_height)

        for i, option in enumerate(self.MENU_OPTIONS):
            line_y = y + 2 + (i * 2)

            with self.term.location(x, line_y):
                pad_left = (self.menu_width - len(option) - 2) // 2
                pad_right = self.menu_width - len(option) - 2 - pad_left
                text = f"{' ' * pad_left}{self.term.reverse}{option}{self.term.normal}{' ' * pad_right}" if i == self.selected_index else f"{' ' * pad_left}{option}{' ' * pad_right}"
                print(f"│{text}│")

    def get_key_map(self):
        return {
            self.term.KEY_UP: lambda: self._move_selection(-1),
            self.term.KEY_DOWN: lambda: self._move_selection(1)
        }

    def _move_selection(self, delta):
        self.selected_index = (self.selected_index + delta) % len(self.MENU_OPTIONS)