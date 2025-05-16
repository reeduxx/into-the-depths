from blessed import Terminal
from client.util import load_ascii_art

def main():
    term = Terminal()
    print(term.clear)
    TITLE_ASCII = load_ascii_art("assets/title.txt")
    
    for line in TITLE_ASCII.splitlines():
        print(term.center(f"{term.green}{line}{term.normal}"))

    return 0

if __name__ == '__main__':
    main()