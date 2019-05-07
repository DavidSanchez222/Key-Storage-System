import uuid


class Container:
    
    def __init__(self, name_page, address, user, password, created_at, updated_at, deleted_at, uid = None):
        self.name_page = name_page
        self.address = address
        self.user = user
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.uid = uid or uuid.uuid4()


    def to_dict(self):
        return vars(self)

    @staticmethod
    def schema():
        return ['uid', 'name_page', 'address', 'user', 'password', 'created_at', 'updated_at', 'deleted_at']