import json

def check_config(filename="config.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print("System Ready.")
        return data

    except FileNotFoundError:
        default_settings = {
            "mode": "default",
            "version": 1.0,
            "debug": False
        }

        with open(filename, "w") as file:
            json.dump(default_settings, file)

        return default_settings


config = check_config()