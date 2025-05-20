import os

def load_ascii_art(relative_path: str) -> str:
    """
    Loads ASCII art from a .txt file.

    Args:
        relative_path (str): Relative path to the .txt file.

    Returns:
        str: The ASCII art as a string.
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    full_path = os.path.join(root_dir, relative_path)

    with open(full_path, 'r', encoding='utf-8') as file:
        return file.read()