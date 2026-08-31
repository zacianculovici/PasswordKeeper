import json

def load_local_data():
    try:
        with open("data/local.json", "r") as file:
            local_data = json.load(file)
    except FileNotFoundError:
        print("Local data file not found. Creating a new one.")
        local_data = {"rememberUsername": False, "connectionToken": None}
        save_local_data(local_data)
    return local_data

def rememberUsername(*args, **kwargs):
    local_data = load_local_data()
    if len(args) > 0:
        remember = args[0]
    elif kwargs.get("value", "empty") != "empty":
        remember = kwargs.get("value")
    else:
        return local_data["rememberUsername"]
    local_data["rememberUsername"] = remember
    save_local_data(local_data)

def save_local_data(local_data):
    with open("data/local.json", "w") as file:
        json.dump(local_data, file, indent=4)
