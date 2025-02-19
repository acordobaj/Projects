class Project:
    def __init__(self, name, description, created_at, consecutive=None, files=None):
        self.consecutive = consecutive
        self.name = name
        self.description = description
        self.created_at = created_at
        self.files = files if files else "Sin archivo"

    def to_dict(self):
        return {
            "consecutive": self.consecutive,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "files": self.files,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            consecutive=data.get("consecutive"),
            name=data.get("name"),
            description=data.get("description"),
            created_at=data.get("created_at"),
            files=data.get("files", "Sin archivo"),
        )
