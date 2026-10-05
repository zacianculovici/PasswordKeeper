import json
import os
from helperFiles.paths import data_path

SALT_FILE_PATH = "salinity.json"

def getSalt(file_path):
    with open(data_path(SALT_FILE_PATH), 'r') as file:
        salt_data = json.load(file)
    return bytes.fromhex(salt_data.get(file_path, ""))

def generateSalt(file_path):
    salt = os.urandom(16)
    with open(data_path(SALT_FILE_PATH), 'r') as file:
        salt_data = json.load(file)
    salt_data[file_path] = salt.hex()
    with open(data_path(SALT_FILE_PATH), 'w') as file:
        json.dump(salt_data, file, indent=4)
    return salt

def removeSalt(file_path):
    with open(data_path(SALT_FILE_PATH), 'r') as file:
        salt_data = json.load(file)
    if file_path in salt_data:
        del salt_data[file_path]
        with open(data_path(SALT_FILE_PATH), 'w') as file:
            json.dump(salt_data, file, indent=4)
