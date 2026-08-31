import os
import json
import helperFiles.objects as objects
from pathlib import Path
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

global debug_mode, salt
salt = b'\x9f\x1c\x8e\x1b\x9d\x1e\x8f\x1c\x9a\x1b\x9d\x1e\x8f\x1c'  # Use a proper salt in production, eg. os.urandom(16) (this can't be generated randomly each time, otherwise the key will change and the data will be unrecoverable. it must be stored somewhere, or derived from a password, etc. maybe in a config file or environment variable. example of a config file: config.json with {"salt": "base64_encoded_salt"} and then load it with json.load(open("config.json"))["salt"].encode() or something like that. or maybe derive it from the username and password, but that might not be secure enough. anyway, just make sure to use a proper salt in production.
debug_mode = "verbose"  # Set to "verbose" for detailed debug output, or "off" for no output

class SecureDataManager:
    def __init__(self, username, password, create=False):
        self.create = create
        self.username = username
        self.password = password
        self.user_data = self.load_user_data(self.username, self.password)

    def load_user_data(self, username, password):
        # Hash the username and password to find the name of the file to load
        self.user = objects.User(username, password)
        hashed_credentials = self.user.hashed_credentials

        file_path = f"data/{hashed_credentials}.enc"
        if not os.path.exists(file_path):
            if self.create:
                self.user_data = {"start_maximised": False, "theme": "blue", "categories": {}, "passwords": {}}
                self.save_user_data()
                return self.user_data
            if debug_mode == "verbose":
                print(f"User data file '{file_path}' does not exist. Creating a new file.")
            raise objects.NoAccountError(f"User data file '{file_path}' does not exist. Please create a new account.")
        else:
            with open(file_path, 'r') as file:
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=390000,
                )
                generated_key = base64.urlsafe_b64encode(kdf.derive((username + password).encode()))
                fernet = Fernet(generated_key)
                encrypted_data = file.read()
                decrypted_data = fernet.decrypt(encrypted_data.encode())
                print(f"Decrypted data for user '{username}': {decrypted_data.decode()}")
                return json.loads(decrypted_data.decode())

    def save_user_data(self):
        hashed_credentials = self.user.hashed_credentials
        file_path = f"data/{hashed_credentials}.enc"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        generated_key = base64.urlsafe_b64encode(kdf.derive((self.username + self.password).encode()))
        fernet = Fernet(generated_key)
        encrypted_data = fernet.encrypt(json.dumps(self.user_data).encode())
        with open(file_path, 'w') as file:
            file.write(encrypted_data.decode())

    def start_maximised(self, *args, **kwargs):
        if len(args) > 0:
            self.user_data["start_maximised"] = args[0]
        elif kwargs.get("value", "empty") != "empty":
            self.user_data["start_maximised"] = kwargs.get("value")
        else:
            return self.user_data["start_maximised"]
        self.save_user_data()

    def theme(self, *args, **kwargs):
        if len(args) > 0:
            self.user_data["theme"] = args[0]
        elif kwargs.get("value", "empty") != "empty":
            self.user_data["theme"] = kwargs.get("value")
        else:
            return self.user_data["theme"]
        self.save_user_data()

    @staticmethod
    def account_exists(username, password):
        user = objects.User(username, password)
        hashed_credentials = user.hashed_credentials
        file_path = f"data/{hashed_credentials}.enc"
        return os.path.exists(file_path)

    @staticmethod
    def username_exists(username):
        global_file_path = Path("data/global.json")
        if not global_file_path.exists():
            print(f"Global file '{global_file_path}' does not exist. Creating a new file.")
            global_data = {"usernames": {}}
            with open(global_file_path, 'w') as file:
                json.dump(global_data, file)
        else:
            with open(global_file_path, 'r') as file:
                global_data = json.load(file)
        return username in global_data.get("usernames", {})

    @staticmethod
    def verify_credentials(username, password):
        if SecureDataManager.username_exists(username):
            if SecureDataManager.account_exists(username, password):
                return True
            else:
                return False
        else:
            return False
