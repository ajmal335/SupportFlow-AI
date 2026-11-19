
import json

from pathlib import Path
from src.config import DATA_DIR


def load_json(filename):
    path = Path(DATA_DIR) / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(filename, data):
    path = Path(DATA_DIR) / filename

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_customers():
    return load_json("customers.json")


def load_orders():
    return load_json("orders.json")


def load_policies():
    path = Path(DATA_DIR) / "policies.txt"

    with open(path, "r", encoding="utf-8") as file:
        return file.read()
