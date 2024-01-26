import hashlib
import random

from src.backend.database import Database


# change passwords for apparats, change passwords for users, list users, create and delete users etc
# create a class that has all commands. for each command, create a function that does the thing
class AdminCommands:
    def __init__(self):
        self.db = Database()

    def create_password(self, password):
        salt = self.create_salt()
        hashed_password = self.hash_password(password)
        return (hashed_password,salt)
    def create_salt(self):
        return "".join(
            random.choices(
                "abcdefghijklmnopqrstuvwxyzQWERTZUIOPLKJHGFDSAYXCVBNM0123456789", k=16
            )
        )

    def create_admin(self):
        salt = self.create_salt()
        hashed_password = self.hash_password("admin")
        self.db.create_user("admin", salt+hashed_password, "admin", salt)
    
    def hash_password(self, password):
        hashed = hashlib.sha256((password).encode("utf-8")).hexdigest()
        return hashed

    def list_users(self):
        return self.db.get_users()

    def delete_user(self, username):
        self.db.delete_user(username)

    def change_password(self, username, password):
        hashed_password = self.hash_password(password)
        self.db.change_password(username, hashed_password)


if __name__ == "__main__":
    c = AdminCommands()
    c.create_user("test", "test", "user")
    c.create_user("admin", "admin", "admin")
    print(c.list_users())
    c.delete_user("test")
    print(c.list_users())
    c.change_password("admin", "nopass")
    print(c.list_users())
