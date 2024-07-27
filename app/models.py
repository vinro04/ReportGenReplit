from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

# Mock user database
users = {
    'admin': {'id': 1, 'password_hash': 'scrypt:32768:8:1$4f8yhlYuNueHB2ks$5e6632b5edc1c9c91f282f3e04afa0b94f0cbb7e27228f7a94bfeee754a98ce3e9514ca7796b79a9496bab4f458e4196b51198ccbe6a38a92ac68e86198f2613'}  # This should be replaced with a hash
}

def get_user(username):
    user_data = users.get(username)
    if user_data:
        return User(user_data['id'], username, user_data['password_hash'])
    return None