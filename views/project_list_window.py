from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from controllers.project_controller import ProjectController


class ProjectListWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project_controller = ProjectController()

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.label_title = Label(text="Project List by Date")
        self.refresh_button = Button(text="Refresh List", on_release=self.refresh_list)
        self.back_button = Button(
            text="Back to Main Menu", on_release=self.back_to_main_menu
        )

        self.layout.add_widget(self.label_title)
        self.layout.add_widget(self.refresh_button)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def refresh_list(self, instance):
        projects = self.project_controller.get_all_projects_sorted_by_date()
        self.layout.clear_widgets()
        self.layout.add_widget(self.label_title)
        self.layout.add_widget(self.refresh_button)
        self.layout.add_widget(self.back_button)
        for project in projects:
            self.layout.add_widget(
                Label(
                    text=f"{project['consecutive']} - {project['name']} - {project.get('status', 'N/A')} - {project['created_at']}"
                )
            )

    def back_to_main_menu(self, instance):
        self.manager.current = "main"
