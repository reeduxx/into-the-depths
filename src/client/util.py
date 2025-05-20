import os
import tomllib

DEFAULT_CONFIG = {
    "theme": "auto"
}

def detect_background() -> str:
    colorfgbg = os.environ.get("COLORFGBG")

    if colorfgbg:
        try:
            fg, bg = map(int, colorfgbg.split(';')[-2:])
            
            if bg >= 10:
                return "light"
        except Exception:
            pass
    
    return "dark"

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

def load_config(path: str = "config/config.toml") -> dict:
    """
    Loads the user config file.

    Args:
        path (str): Relative path the config.toml file.
    
    Returns:
        dict: A dictionary containing the config file keys and values.
    """
    if not os.path.exists(path):
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(path, "rb") as file:
            user_config = tomllib.load(file)
    except Exception:
        return DEFAULT_CONFIG.copy()

    return {**DEFAULT_CONFIG, **user_config}