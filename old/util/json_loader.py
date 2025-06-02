import json
import os

def load_json(type_name, filename):
    filepath = os.path.join(f"old/data/{type_name}", filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: {filepath} not found.")
    
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)