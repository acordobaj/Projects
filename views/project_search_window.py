from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from controllers.project_controller import ProjectController


class ProjectSearchWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project_controller = ProjectController()

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.label_title = Label(text="Search Project by Consecutive")
        self.consecutive_input = TextInput(
            hint_text="Enter Consecutive", multiline=False
        )
        self.search_button = Button(text="Search", on_release=self.search_project)
        self.back_button = Button(
            text="Back to Main Menu", on_release=self.back_to_main_menu
        )

        self.layout.add_widget(self.label_title)
        self.layout.add_widget(self.consecutive_input)
        self.layout.add_widget(self.search_button)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def search_project(self, instance):
        consecutive = self.consecutive_input.text
        project = self.project_controller.get_project_by_consecutive(consecutive)
        if project:
            self.layout.add_widget(
                Label(
                    text=f"{project.consecutive} - {project.name} - {project.status} - {project.created_at}"
                )
            )
        else:
            self.layout.add_widget(Label(text="Project not found"))

    def back_to_main_menu(self, instance):
        self.manager.current = "main"
