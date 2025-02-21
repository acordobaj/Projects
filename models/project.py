from datetime import datetime


class Project:
    def __init__(
        self,
        consecutive,
        name,
        description,
        files,
        created_at=None,
        status="En Proceso",
    ):
        self.consecutive = consecutive
        self.name = name
        self.description = description
        self.files = files
        self.created_at = created_at or datetime.utcnow()
        self.status = status

    @classmethod
    def from_dict(cls, data):
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        return cls(
            data["consecutive"],
            data["name"],
            data["description"],
            data["files"],
            created_at,
            data.get("status", "En Proceso"),
        )

    def to_dict(self):
        return {
            "consecutive": self.consecutive,
            "name": self.name,
            "description": self.description,
            "files": self.files,
            "created_at": self.created_at,
            "status": self.status,
        }
