
def load_ascii_art(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()