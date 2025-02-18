from pymongo import MongoClient
from datetime import datetime

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
db = client["project_management"]

# Obtener la colección de proyectos
projects = db["projects"]

# Actualizar documentos que no tienen el campo 'created_at'
projects.update_many(
    {"created_at": {"$exists": False}},
    {"$set": {"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}},
)

# Actualizar documentos que no tienen el campo 'consecutive'
cursor = projects.find({"consecutive": {"$exists": False}})
consecutive = 1
for project in cursor:
    projects.update_one({"_id": project["_id"]}, {"$set": {"consecutive": consecutive}})
    consecutive += 1

print("Database migration completed.")
