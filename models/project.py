class Project:
    def __init__(self, name, status, created_at, consecutive=None):
        self.consecutive = consecutive
        self.name = name
        self.status = status
        self.created_at = created_at

    def to_dict(self):
        return {
            "consecutive": self.consecutive,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            consecutive=data.get("consecutive"),
            name=data.get("name"),
            status=data.get("status"),
            created_at=data.get("created_at"),
        )
