import hashlib


class User:

    def __init__(self, username, password):
        self.username = hashlib.sha256(username.encode('utf8')).hexdigest()
        self.password = hashlib.sha256(password.encode('utf8')).hexdigest()