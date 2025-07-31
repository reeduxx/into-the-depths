from .menu import Menu

class ActionMenu(Menu):
    """
    A Pokémon-style 2x2 action menu (Fight, Bag, etc.).
    """
    def __init__(self, term, config):
        super().__init__(term)
        self.options = [["Attack", "Pouch"], ["Advice", "Run"]]
        self.selected_row = 0
        self.selected_col = 0
        self.selected_action = None
        self.config = config

    def run(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            self.buffer.clear()
            
            while True:
                self.display_menu()
                self.buffer.render()
                key = self.term.inkey(timeout=0.1)
                if self.handle_input(key):
                    break

        return self.selected_action

    def display_menu(self):
        box_width = 30
        box_height = 6
        box_x = (self.term.width - box_width) // 2
        box_y = (self.term.height - box_height) // 2

        self.draw_box(box_x, box_y, box_width, box_height)
        self.buffer.draw_text(box_x + 2, box_y + 1, "Choose an action")

        for row in range(2):
            for col in range(2):
                label = self.options[row][col]
                is_selected = (row == self.selected_row and col == self.selected_col)
                style = self.term.reverse if is_selected else ""
                x_offset = 2 + col * 12
                y_offset = box_y + 2 + row
                self.buffer.draw_text(box_x + x_offset, y_offset, label, style)

    def handle_input(self, key):
        if key.code == self.term.KEY_UP and self.selected_row > 0:
            self.selected_row -= 1
        elif key.code == self.term.KEY_DOWN and self.selected_row < 1:
            self.selected_row += 1
        elif key.code == self.term.KEY_LEFT and self.selected_col > 0:
            self.selected_col -= 1
        elif key.code == self.term.KEY_RIGHT and self.selected_col < 1:
            self.selected_col += 1
        elif key.code == self.term.KEY_ENTER or key == '\n':
            self.selected_action = self.options[self.selected_row][self.selected_col].lower()
            return True
        return False
