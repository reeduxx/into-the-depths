from client.menu.menu import Menu

class JoinMenu(Menu):
    def __init__(self, term, config):
        super().__init__(term)
        self.config = config
        self.theme = self.config.get("theme", "auto")
        self.max_ip_length = 15
        self.ip_string = ""
        self.num_confirmed = False

    def run(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            self.buffer.clear()

            while True:
                self.display_menu()
                self.buffer.render()
                key = self.term.inkey(timeout=0.1)
                if self.handle_input(key):
                    break

    def display_menu(self):
        
        box_width = self.max_ip_length + 10
        box_x = (self.term.width - box_width) // 2
        box_y = 12
        self.draw_box(box_x, box_y, box_width, 4)
        ip_display = "Enter IP: " + self.ip_string + ('_' if not self.num_confirmed else ' ') * (self.max_ip_length - len(self.ip_string))
        ip_x = (self.term.width - len(ip_display)) // 2
        ip_y = box_y + 2
        self.buffer.draw_text(ip_x, ip_y, ip_display)

    def handle_input(self, key):
        if key.code == self.term.KEY_ENTER and self.ip_string:
            self.num_confirmed = True
            print(f"Joining server using ip: {self.ip_string}")
            self.join_server()
            return True
        elif key.code == self.term.KEY_BACKSPACE and self.ip_string:
            self.ip_string = self.ip_string[:-1]
        elif (key.isalnum() or key.code == 32 or key == ' ') and len(self.ip_string) < self.max_ip_length:
            self.ip_string += key
        return False

    #TODO implement server joining code using this method
    def join_server(self):
        pass