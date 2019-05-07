import uuid

from datetime import datetime


class Container:
    
    def __init__(self, name_page, address, user, password):
        self.name_page = name_page
        self.address = address
        self.user = user
        self.password = password
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.deleted_at = None
        self.uid = uuid.uuid4()


    def to_dict(self):
        return vars(self)

    @staticmethod
    def schema():
        return ['uid', 'name_page', 'address', 'user', 'password', 'created_at', 'updated_at', 'deleted_at']