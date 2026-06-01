from pathlib import Path
import pytest


@pytest.fixture(autouse=True)
def temp_storage(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("students.json").write_text("[]")
    return tmp_path

@pytest.fixture
def students():
    return [
        {"name": "amjad", "email": "amjad@example.com", "age": 20},
    ]