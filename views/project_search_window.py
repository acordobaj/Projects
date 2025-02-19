from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from controllers.project_controller import ProjectController


class ProjectSearchWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project_controller = ProjectController()

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        menu_layout = BoxLayout(
            orientation="horizontal", padding=10, spacing=10, size_hint=(1, 0.1)
        )
        content_layout = BoxLayout(
            orientation="vertical", padding=10, spacing=10, size_hint=(1, 0.9)
        )

        self.label_title = Label(text="Search Project by Consecutive")
        self.consecutive_input = TextInput(
            hint_text="Enter Consecutive", multiline=False
        )
        self.search_button = Button(text="Search", on_release=self.search_project)
        self.back_button = Button(
            text="Back to Main Menu", on_release=self.back_to_main_menu
        )

        menu_layout.add_widget(self.label_title)
        menu_layout.add_widget(self.consecutive_input)
        menu_layout.add_widget(self.search_button)
        menu_layout.add_widget(self.back_button)

        self.layout_content = ScrollView()
        self.content_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.layout_content.add_widget(self.content_layout)

        layout.add_widget(menu_layout)
        layout.add_widget(self.layout_content)

        self.add_widget(layout)

    def search_project(self, instance):
        consecutive = self.consecutive_input.text
        project = self.project_controller.get_project_by_consecutive(consecutive)
        self.content_layout.clear_widgets()
        if project:
            project_info = f"{project.consecutive} - {project.name} - {project.description} - {project.created_at}"
            if project.file_links:
                for file_link in project.file_links:
                    project_info += f"\n   File: {file_link}"
            self.content_layout.add_widget(Label(text=project_info))
        else:
            self.content_layout.add_widget(Label(text="Project not found"))

    def back_to_main_menu(self, instance):
        self.manager.current = "main"
