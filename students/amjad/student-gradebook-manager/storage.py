import json


def load_students() -> list[dict]:
    with open("students.json", "r") as f:
        return json.load(f)


def to_json(students: list[dict]) -> None:
    with open("students.json", "w") as f:
        json.dump(students, f, indent=4)
