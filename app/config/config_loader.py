# /config/config_loader.py

import json
import os

def load_punishment_doctrine():
    """Load punishment doctrine from config file."""
    path = os.path.join(os.path.dirname(__file__), "punishment_doctrine.json")
    with open(path, "r") as f:
        doctrine = json.load(f)
    return doctrine
