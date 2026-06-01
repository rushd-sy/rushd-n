"""
To hanlde JSON rade/write operations
"""
import json

def read_data(path="gradebook.json") -> dict:        
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        default_data = {"students": []}
        write_data(default_data)
        return default_data
    except json.JSONDecodeError:
        default_data = {"students": []}
        write_data(default_data)
        return default_data
    except Exception as e:
        raise RuntimeError(f"There was a problem while trying to open gradebook.json.\n{e}")

def write_data(data: dict, path="gradebook.json") -> None:
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
