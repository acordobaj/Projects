from database.db_manager import DBManager
from models.project import Project
from datetime import datetime


class ProjectController:
    def __init__(self):
        self.db_manager = DBManager()
        self.projects_collection = self.db_manager.get_collection("projects")

    def create_project(self, project):
        project.consecutive = self.get_next_consecutive()
        if not hasattr(project, "created_at"):
            project.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.projects_collection.insert_one(project.to_dict())

    def update_project(self, project, name, description):
        self.projects_collection.update_one(
            {"consecutive": project.consecutive},
            {"$set": {"name": name, "description": description}},
        )

    def get_project_by_consecutive(self, consecutive):
        project_data = self.projects_collection.find_one(
            {"consecutive": int(consecutive)}
        )
        if project_data:
            return Project.from_dict(project_data)
        return None

    def delete_project(self, consecutive):
        self.projects_collection.delete_one({"consecutive": int(consecutive)})

    def get_all_projects_sorted_by_date(self):
        all_projects = self.projects_collection.find()
        sorted_projects = sorted(
            all_projects,
            key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%d %H:%M:%S"),
        )
        return sorted_projects

    def get_next_consecutive(self):
        last_project = self.projects_collection.find_one(sort=[("consecutive", -1)])
        return last_project["consecutive"] + 1 if last_project else 1
