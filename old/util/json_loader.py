import json
import os

def load_json(type_name, filename):
    filepath = os.path.join(f"src/data/{type_name}", filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: data/{type_name}/{filename} not found.")
    
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)