from pymongo import MongoClient


class DatabaseMigration:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def convert_file_field_to_string(self):
        all_projects = self.collection.find()
        for project_data in all_projects:
            if isinstance(project_data.get("files", None), list):
                file_list = project_data["files"]
                if file_list:
                    file_string = file_list[
                        0
                    ]  # Assuming the first file in the list is the desired one
                else:
                    file_string = "Sin archivo"
                self.collection.update_one(
                    {"_id": project_data["_id"]}, {"$set": {"files": file_string}}
                )


if __name__ == "__main__":
    db_migration = DatabaseMigration(
        db_name="project_management", collection_name="projects"
    )
    db_migration.convert_file_field_to_string()
    print("Database migration completed.")
