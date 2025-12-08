# utils/language.py
import json
from .resources import resource_path

def load_language_data():
    path = resource_path("languages.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)