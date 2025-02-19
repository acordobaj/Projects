from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from controllers.project_controller import ProjectController
import webbrowser
import os


class ProjectListWindow(Screen):
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

        self.label_title = Label(text="Project List by Date")
        self.refresh_button = Button(text="Refresh List", on_release=self.refresh_list)
        self.back_button = Button(
            text="Back to Main Menu", on_release=self.back_to_main_menu
        )

        menu_layout.add_widget(self.label_title)
        menu_layout.add_widget(self.refresh_button)
        menu_layout.add_widget(self.back_button)

        self.layout_content = ScrollView()
        self.content_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.layout_content.add_widget(self.content_layout)

        layout.add_widget(menu_layout)
        layout.add_widget(self.layout_content)

        self.add_widget(layout)

    def refresh_list(self, instance):
        # Actualizar la base de datos con los enlaces de archivos
        self.project_controller.update_all_projects_with_files()

        projects = self.project_controller.get_all_projects_sorted_by_date()
        self.content_layout.clear_widgets()
        for project in projects:
            project_info = f"{project['consecutive']} - {project['name']} - {project.get('description', 'N/A')} - {project['created_at']}"
            file_link = project.get("files", "Sin archivo")
            project_info += f"\n   File: {file_link}"
            project_label = Label(text=project_info)

            project_box = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=project_label.texture_size[1] + 20,
            )
            project_box.add_widget(project_label)

            if file_link != "Sin archivo":
                open_file_button = Button(
                    text="Open File",
                    size_hint=(None, None),
                    size=(100, 40),
                    on_release=lambda instance, file_link=file_link: self.open_file(
                        file_link
                    ),
                )
                project_box.height += open_file_button.height + 10
                project_box.add_widget(open_file_button)

            self.content_layout.add_widget(project_box)

    def back_to_main_menu(self, instance):
        self.manager.current = "main"

    def open_file(self, file_link):
        if file_link != "Sin archivo":
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "project_files",
                file_link,
            )
            if os.path.exists(file_path):
                webbrowser.open(f"file://{file_path}")
            else:
                popup = Popup(
                    title="Error",
                    content=Label(text="File not found."),
                    size_hint=(None, None),
                    size=(400, 200),
                )
                popup.open()
        else:
            popup = Popup(
                title="Error",
                content=Label(text="No file associated with this project."),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()
