import os
from datetime import datetime
from database.db_manager import DBManager
from models.project import Project


class ProjectController:
    def __init__(self):
        self.db_manager = DBManager()
        self.projects_collection = self.db_manager.get_collection("projects")
        self.project_files_path = "project_files"

    def create_project(self, name, description, status):
        # Obtener el siguiente número consecutivo
        last_project = self.projects_collection.find_one(sort=[("consecutive", -1)])
        next_consecutive = last_project["consecutive"] + 1 if last_project else 1

        # Verificar si el archivo existe
        file_name = f"{next_consecutive}_proyecto.pdf"
        file_path = os.path.join(self.project_files_path, file_name)
        files = file_name if os.path.exists(file_path) else "Sin archivo"

        # Crear el proyecto con la fecha de creación actual
        new_project = Project(
            next_consecutive, name, description, files, datetime.utcnow(), status
        )
        self.projects_collection.insert_one(new_project.to_dict())

    def get_projects(self):
        projects = list(self.projects_collection.find())
        updated_projects = []
        for project in projects:
            updated_project = self.check_and_update_file(project)
            updated_projects.append(updated_project)
        return [Project.from_dict(project) for project in updated_projects]

    def check_and_update_file(self, project):
        file_name = f"{project['consecutive']}_proyecto.pdf"
        file_path = os.path.join(self.project_files_path, file_name)
        if os.path.exists(file_path):
            if project["files"] == "Sin archivo":
                self.projects_collection.update_one(
                    {"consecutive": project["consecutive"]},
                    {"$set": {"files": file_name}},
                )
                project["files"] = file_name
        return project

    def filter_projects(self, name_filter=None, month_filter=None):
        query = {}
        if name_filter:
            query["name"] = {"$regex": name_filter, "$options": "i"}
        if month_filter:
            query["$expr"] = {"$eq": [{"$month": "$created_at"}, month_filter]}

        projects = list(self.projects_collection.find(query))
        updated_projects = []
        for project in projects:
            updated_project = self.check_and_update_file(project)
            updated_projects.append(updated_project)
        return [Project.from_dict(project) for project in updated_projects]

    def delete_project(self, consecutive):
        self.projects_collection.delete_one({"consecutive": consecutive})
