from pymongo import MongoClient


def create_database():
    # Conexión a MongoDB (ajusta la URI según tu configuración)
    client = MongoClient("mongodb://localhost:27017/")

    # Crear la base de datos
    db = client["my_database"]

    # Crear la colección de usuarios y agregar algunos datos de ejemplo
    users_collection = db["users"]
    users_collection.insert_many(
        [
            {"username": "user1", "password": "pass1", "role": "admin"},
            {"username": "user2", "password": "pass2", "role": "user"},
        ]
    )

    # Crear la colección de proyectos y agregar algunos datos de ejemplo
    projects_collection = db["projects"]
    projects_collection.insert_many(
        [
            {
                "consecutive": 1,
                "name": "Proyecto 1",
                "description": "Descripción del Proyecto 1",
                "files": "1_proyecto.pdf",
                "created_at": "2025-02-20T22:11:25",
                "status": "activo",
            },
            {
                "consecutive": 2,
                "name": "Proyecto 2",
                "description": "Descripción del Proyecto 2",
                "files": "Sin archivo",
                "created_at": "2025-02-20T22:11:25",
                "status": "inactivo",
            },
        ]
    )

    print("Base de datos y colecciones creadas con éxito")


if __name__ == "__main__":
    create_database()
