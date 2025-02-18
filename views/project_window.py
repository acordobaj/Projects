from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from controllers.project_controller import ProjectController
from models.project import Project
from datetime import datetime


class ProjectWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project_controller = ProjectController()

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.name_input = TextInput(hint_text="Project Name", multiline=False)
        self.status_input = Spinner(
            text="Select Status", values=("Listo", "Cancelado", "En progreso")
        )
        self.save_button = Button(text="Save", on_release=self.save_project)
        self.back_button = Button(
            text="Back to Main Menu", on_release=self.back_to_main_menu
        )

        layout.add_widget(Label(text="Create Project"))
        layout.add_widget(self.name_input)
        layout.add_widget(self.status_input)
        layout.add_widget(self.save_button)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def save_project(self, instance):
        name = self.name_input.text
        status = self.status_input.text
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_project = Project(name=name, status=status, created_at=created_at)
        self.project_controller.create_project(new_project)
        Popup(
            title="Success",
            content=Label(text="Project created successfully"),
            size_hint=(0.75, 0.5),
        ).open()
        self.manager.current = "main"

    def back_to_main_menu(self, instance):
        self.manager.current = "main"
