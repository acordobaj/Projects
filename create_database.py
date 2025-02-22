from pymongo import MongoClient
from datetime import datetime

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Seleccionar la base de datos
db = client.proyectosDB

# Crear colección de usuarios y añadir documentos de ejemplo
usuarios = db.usuarios
usuarios.insert_many([
    {
        "username": "admin",
        "password": "password",
        "role": "Admin",
        "createdAt": datetime.now()
    },
    {
        "username": "usuario1",
        "password": "password1",
        "role": "User",
        "createdAt": datetime.now()
    }
])

# Crear colección de proyectos y añadir documentos de ejemplo
proyectos = db.proyectos
proyectos.insert_many([
    {
        "nombre": "Proyecto 1",
        "descripcion": "Descripción del Proyecto 1",
        "archivos": "archivo1.pdf",
        "estatus": "Activo",
        "createdAt": datetime.now(),
        "createdBy": "admin"
    },
    {
        "nombre": "Proyecto 2",
        "descripcion": "Descripción del Proyecto 2",
        "archivos": "archivo2.pdf",
        "estatus": "Inactivo",
        "createdAt": datetime.now(),
        "createdBy": "usuario1"
    }
])

print("Base de datos y colecciones creadas exitosamente.")