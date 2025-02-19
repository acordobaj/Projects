from pymongo import MongoClient
from datetime import datetime

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
db = client["project_management"]

# Crear colección de usuarios
users = db["users"]
users.drop()  # Eliminar la colección si ya existe

# Insertar datos de ejemplo en la colección de usuarios
users.insert_many(
    [
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "user1", "password": "user123", "role": "basic"},
        {"username": "user2", "password": "user123", "role": "media"},
    ]
)

# Crear colección de proyectos
projects = db["projects"]
projects.drop()  # Eliminar la colección si ya existe

# Insertar datos de ejemplo en la colección de proyectos
projects.insert_many(
    [
        {
            "consecutive": 1,
            "name": "Project1",
            "description": "Description1",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        {
            "consecutive": 2,
            "name": "Project2",
            "description": "Description2",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        {
            "consecutive": 3,
            "name": "Project3",
            "description": "Description3",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    ]
)

print("Database setup completed.")
