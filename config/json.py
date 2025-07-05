import json

def load(json_path: str):
    with open(json_path) as f:
         return json.load(f)