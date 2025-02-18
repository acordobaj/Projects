from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from controllers.project_controller import ProjectController
from models.project import Project


class ModifyProjectWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project_controller = ProjectController()

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.name_input = TextInput(hint_text="Project Name", multiline=False)
        self.description_input = TextInput(hint_text="New Description", multiline=True)
        self.modify_button = Button(text="Modify", on_release=self.modify_project)
        self.back_button = Button(
            text="Back to Main Menu", on_release=self.back_to_main_menu
        )

        layout.add_widget(Label(text="Modify Project"))
        layout.add_widget(self.name_input)
        layout.add_widget(self.description_input)
        layout.add_widget(self.modify_button)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def modify_project(self, instance):
        name = self.name_input.text
        description = self.description_input.text
        project = self.project_controller.get_project(name)
        if project:
            self.project_controller.update_project(project, name, description)
            Popup(
                title="Success",
                content=Label(text="Project modified successfully"),
                size_hint=(0.75, 0.5),
            ).open()
            self.manager.current = "main"
        else:
            Popup(
                title="Error",
                content=Label(text="Project not found"),
                size_hint=(0.75, 0.5),
            ).open()

    def back_to_main_menu(self, instance):
        self.manager.current = "main"
