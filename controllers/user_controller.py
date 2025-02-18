from database.db_manager import DBManager
from models.user import User


class UserController:
    def __init__(self):
        self.db_manager = DBManager()
        self.users_collection = self.db_manager.get_collection("users")

    def login(self, username, password):
        user_data = self.users_collection.find_one(
            {"username": username, "password": password}
        )
        if user_data:
            return User.from_dict(user_data)
        return None

    def create_user(self, username, password, role):
        new_user = User(username, password, role)
        self.users_collection.insert_one(new_user.to_dict())

    def get_user(self, username):
        user_data = self.users_collection.find_one({"username": username})
        if user_data:
            return User.from_dict(user_data)
        return None

    def update_user(self, user, password, role):
        if password:
            user.password = password
        user.role = role
        self.users_collection.update_one(
            {"username": user.username},
            {"$set": {"password": user.password, "role": user.role}},
        )

    def delete_user(self, username):
        self.users_collection.delete_one({"username": username})
