import hashlib, os

from config.model import User

class AuthService:


    def __init__(self, username, password):
        self.username = username
        self.password = password

    
    def create_user(self, user):
        with open('.env', mode = 'a') as f:
            f.write(f'KSS_USER={user.username}\n')
            f.write(f'KSS_PASSWD={user.password}\n')
        
    

    def verify_user(self, username, password):
        username = hashlib.sha256(username.encode('utf8')).hexdigest()
        password = hashlib.sha256(password.encode('utf8')).hexdigest()
        if self.username == None or self.password == None:
            return None
        else:
            if self.username == username and self.password == password:
                return True
            else:
                return False
            


    def update_user(self, user_updated):
        with open('.env', mode = 'r') as f:
            for row in f.readlines():
                if 'USER' in row:
                    row = f'KSS_USER={user_updated.username}\n'
                elif 'PASSWD' in row:
                    row = f'KSS_PASSWD={user_updated.password}\n'
                
                with open('.env.tmp', mode = 'a') as f:
                    f.write(row)
        os.remove('.env')
        os.rename('.env.tmp', '.env')