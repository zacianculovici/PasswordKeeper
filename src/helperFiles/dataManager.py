import os
import json

global debug_mode
debug_mode = "off"  # Set to "verbose" for detailed debug output, or "silent" for no output

class DataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_data = self.load_file_data()

    def __setattr__(self, name, value):
        if debug_mode == "verbose":
            print(f"Setting attribute '{name}' to '{value}'")
        super().__setattr__(name, value)
        if name != "file_path":
            self.save_file_data()

    def load_file_data(self):
        if not os.path.exists("./" + self.file_path):
            if debug_mode == "verbose":
                print(f"File '{self.file_path}' does not exist. Creating a new file.")
            # create the file if it doesn't exist
            with open(self.file_path, 'w') as file:
                json.dump({}, file)
            return {}
        with open(self.file_path, 'r') as file:
            try:
                if debug_mode == "verbose":
                    print(f"Loading data from file '{self.file_path}'.")
                return json.load(file)
            except json.JSONDecodeError as e:
                if debug_mode == "verbose":
                    print(f"Error decoding JSON from file '{self.file_path}': {e}. Returning empty dictionary.")
                return {}

    def save_file_data(self):
        if debug_mode == "verbose":
            print(f"Saving data to file '{self.file_path}': {self.file_data}")
        with open(self.file_path, 'w') as file:
            json.dump(self.file_data, file, indent=4)
                

# =============== unused ===============

# class UserDataManager(DataManager):
#     def __init__(self, file_path=None):
#         super().__init__(file_path)

#     def get_user_data(self, username):
#         return self.file_data.get(username, {})

#     def set_user_data(self, username, data):
#         self.file_data[username] = data

#     def add_password_entry(self, username, entry):
#         user_data = self.get_user_data(username)
#         if 'passwords' not in user_data:
#             user_data['passwords'] = []
#         user_data['passwords'].append(entry)
#         self.set_user_data(username, user_data)

#     def remove_password_entry(self, username, entry):
#         user_data = self.get_user_data(username)
#         if 'passwords' in user_data and entry in user_data['passwords']:
#             user_data['passwords'].remove(entry)
#             self.set_user_data(username, user_data)

#     def add_category(self, username, category):
#         user_data = self.get_user_data(username)
#         if 'categories' not in user_data:
#             user_data['categories'] = []
#         if category not in user_data['categories']:
#             user_data['categories'].append(category)
#             self.set_user_data(username, user_data)

#     def remove_category(self, username, category):
#         user_data = self.get_user_data(username)
#         if 'categories' in user_data and category in user_data['categories']:
#             user_data['categories'].remove(category)
#             self.set_user_data(username, user_data)

#     def get_categories(self, username):
#         user_data = self.get_user_data(username)
#         return user_data.get('categories', [])