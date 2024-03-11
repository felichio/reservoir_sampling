import json
import os

CONFIG_FILE = "config.json"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), CONFIG_FILE)

with open(CONFIG_PATH) as f:
    settings = json.load(f)
    # modify input path
    settings["input"] = os.path.join(os.path.dirname(__file__), "..", "input", settings["input"])

