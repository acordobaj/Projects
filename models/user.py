class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username"),
            password=data.get("password"),
            role=data.get("role")
        )