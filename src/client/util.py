
def load_ascii_art(filename: str) -> str:
    """
    Loads ASCII art from a .txt file.

    Args:
        filename (str): Relative path to the .txt file.

    Returns:
        str: The ASCII art as a string.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()