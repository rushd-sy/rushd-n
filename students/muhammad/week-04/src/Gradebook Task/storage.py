"""
To handle JSON read/write operations
"""
import json
import os

def get_db_path() -> str:
    return os.getenv("GRADEBOOK_DB", "gradebook.json")

def read_data() -> dict[str, list]:
    path = get_db_path()
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        default_data = {"students": []}
        write_data(default_data)
        return default_data
    except Exception as e:
        raise RuntimeError(f"There was a problem while trying to open {path}.\n{e}")

def write_data(data: dict) -> None:
    path = get_db_path()
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
