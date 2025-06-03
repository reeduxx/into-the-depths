from client.menu.menu import Menu
import sys

class MultiplayerMenu(Menu):
    def __init__(self, term, config):
        super().__init__(term)  # Initialize Menu base class
        self.config = config
    def run(self):
        options = ["Join", "Host", "Back"]
        index = 0

        box_width = 30
        box_height = len(options) + 4
        box_x = (self.term.width - box_width) // 2
        box_y = (self.term.height - box_height) // 2

        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                self.clear_screen()
                
                # Draw the box
                self.draw_box(box_x, box_y, box_width, box_height)
                
                # Draw each menu option centered within the box
                for i, option in enumerate(options):
                    style = self.term.reverse if i == index else ""
                    y = box_y + 2 + i
                    
                    # Center the text within the box
                    # Available width inside box = box_width - 2 (for left/right borders)
                    available_width = box_width - 2
                    text_x = box_x + 1 + (available_width - len(option)) // 2
                    
                    self.buffer.draw_text(text_x, y, option, style)

                # Render the frame
                self.buffer.render()

                key = self.term.inkey()
                if key.code == self.term.KEY_UP:
                    index = (index - 1) % len(options)
                elif key.code == self.term.KEY_DOWN:
                    index = (index + 1) % len(options)
                elif key.name == "ENTER":
                    return options[index].lower()
                elif key.lower() == "q":
                    return "back"