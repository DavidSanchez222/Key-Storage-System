import uuid

from datetime import datetime


class Container:
    
    def __init__(self, name_page, address, user, password, created_at = None, updated_at = None, deleted_at = None, uid = None):
        self.name_page = name_page
        self.address = address
        self.user = user
        self.password = password
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.deleted_at = deleted_at or 0
        self.uid = uid or uuid.uuid4()


    def to_dict(self):
        return vars(self)

    @staticmethod
    def schema():
        return ['uid', 'name_page', 'address', 'user', 'password', 'created_at', 'updated_at', 'deleted_at']