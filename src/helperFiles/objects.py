import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.hashed_credentials = self.get_hashed_credentials(username, password)

    @staticmethod
    def get_hashed_credentials(username, password):
        credentials = username + password
        return hashlib.sha256(credentials.encode()).hexdigest()

class NoAccountError(Exception):
    """Exception raised when a user account does not exist."""
    def __init__(self, message="User account does not exist. Please create a new account."):
        self.message = message
        super().__init__(self.message)