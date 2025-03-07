from pathlib import Path
from appdirs import user_data_dir

GAME_NAME = "Into the Depths"
VERSION = "0.0.1-a"
SAVE_DIR = Path(user_data_dir(GAME_NAME, appauthor=False)) / "saves"
SAVE_DIR.mkdir(parents=True, exist_ok=True)