import json

def save_inventory(data, filename="inventory.json"):
    with open(filename, "w") as file:
        json.dump(data, file)

def load_inventory(filename="inventory.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

inventory = {"apple": 10, "banana": 5}
save_inventory(inventory)

loaded_data = load_inventory()
print(loaded_data)