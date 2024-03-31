from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Sample User Model (Replace with your database model)
class User(UserMixin):
    def __init__(self, username, password=None):
        self.username = username
        self.password = password

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)
