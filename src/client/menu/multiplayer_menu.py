import blessed

class MultiplayerMenu:
    def __init__(self, term, config):
        self.term = term
        self.config = config

    def run(self):
        options = ["Join", "Host", "Back"]
        index = 0

        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                print(self.term.clear)
                print(self.term.move_y(self.term.height // 2 - 2))
                for i, option in enumerate(options):
                    if i == index:
                        print(self.term.center(self.term.reverse(option)))
                    else:
                        print(self.term.center(option))

                key = self.term.inkey()
                if key.code == self.term.KEY_UP:
                    index = (index - 1) % len(options)
                elif key.code == self.term.KEY_DOWN:
                    index = (index + 1) % len(options)
                elif key.name == "ENTER":
                    return options[index].lower()
                elif key.lower() == "q":
                    return "back"
