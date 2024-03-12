import json
import os
import copy

CONFIG_FILE = "config.json"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), CONFIG_FILE)

with open(CONFIG_PATH) as f:
    settings = json.load(f)
    settings_copy = copy.deepcopy(settings)
    # modify input path
    settings["input"] = os.path.join(os.path.dirname(__file__), "..", "input", settings["input"])


def get_output_folder():
    no = settings_copy["output_directory_number"]
    settings_copy["output_directory_number"] += 1
    with open(CONFIG_PATH, "w", encoding = "utf-8") as f:
        json.dump(settings_copy, f, indent = 4)
    return no
    