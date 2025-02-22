import os
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient(
    "mongodb://localhost:27017/"
)  # Asegúrate de que MongoDB esté en localhost:27017
db = client["project_management"]  # Base de datos

# Colecciones
users_collection = db["users"]
projects_collection = db["projects"]


def update_project_files():
    """
    Actualiza el campo 'files' en la colección 'projects'
    basándose en los archivos en la carpeta 'project_files'.
    """
    project_files_dir = "project_files"  # Carpeta donde se almacenan los archivos

    # Verifica si la carpeta existe
    if not os.path.exists(project_files_dir):
        print(f"La carpeta '{project_files_dir}' no existe.")
        return

    # Lista todos los archivos en la carpeta
    files_in_folder = os.listdir(project_files_dir)

    # Recorre todos los proyectos en la colección
    for project in projects_collection.find():
        consecutive = str(project["consecutive"])  # Consecutivo del proyecto

        # Busca un archivo cuyo nombre contenga el consecutivo
        matching_file = None
        for file_name in files_in_folder:
            if consecutive in file_name:
                matching_file = file_name
                break

        # Actualiza el campo 'files' en la base de datos
        if matching_file:
            projects_collection.update_one(
                {"_id": project["_id"]}, {"$set": {"files": matching_file}}
            )
            print(
                f"Actualizado proyecto {project['name']} con archivo: {matching_file}"
            )
        else:
            # Si no hay archivo, establece 'files' como "Sin archivo"
            projects_collection.update_one(
                {"_id": project["_id"]}, {"$set": {"files": "Sin archivo"}}
            )
            print(f"Proyecto {project['name']} sin archivo asociado.")
