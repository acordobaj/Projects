from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController


class MainWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project_controller = ProjectController()
        self.user_controller = UserController()
        self.user = None

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Crear menús desplegables para User y Project
        user_dropdown = DropDown()
        self.create_user_button = Button(text="Create", size_hint_y=None, height=44)
        self.modify_user_button = Button(text="Modify", size_hint_y=None, height=44)
        self.delete_user_button = Button(text="Delete", size_hint_y=None, height=44)
        user_dropdown.add_widget(self.create_user_button)
        user_dropdown.add_widget(self.modify_user_button)
        user_dropdown.add_widget(self.delete_user_button)

        user_main_button = Button(text="User", size_hint=(None, None))
        user_main_button.bind(on_release=user_dropdown.open)
        user_dropdown.bind(
            on_select=lambda instance, x: setattr(user_main_button, "text", x)
        )

        project_dropdown = DropDown()
        self.create_project_button = Button(text="Create", size_hint_y=None, height=44)
        self.modify_project_button = Button(text="Modify", size_hint_y=None, height=44)
        self.delete_project_button = Button(text="Delete", size_hint_y=None, height=44)
        self.project_list_button = Button(
            text="List by Date", size_hint_y=None, height=44
        )
        self.project_search_button = Button(
            text="Consecutive", size_hint_y=None, height=44
        )
        project_dropdown.add_widget(self.create_project_button)
        project_dropdown.add_widget(self.modify_project_button)
        project_dropdown.add_widget(self.delete_project_button)
        project_dropdown.add_widget(self.project_list_button)
        project_dropdown.add_widget(self.project_search_button)

        project_main_button = Button(text="Project", size_hint=(None, None))
        project_main_button.bind(on_release=project_dropdown.open)
        project_dropdown.bind(
            on_select=lambda instance, x: setattr(project_main_button, "text", x)
        )

        menu_layout = BoxLayout(
            orientation="horizontal", padding=10, spacing=10, size_hint=(1, 0.1)
        )
        menu_layout.add_widget(user_main_button)
        menu_layout.add_widget(project_main_button)

        self.content_layout = BoxLayout(
            orientation="vertical", padding=10, spacing=10, size_hint=(1, 0.9)
        )

        layout.add_widget(menu_layout)
        layout.add_widget(self.content_layout)

        self.add_widget(layout)

        self.create_user_button.bind(on_release=self.go_to_create_user)
        self.modify_user_button.bind(on_release=self.go_to_modify_user)
        self.delete_user_button.bind(on_release=self.delete_user)
        self.create_project_button.bind(on_release=self.go_to_create_project)
        self.modify_project_button.bind(on_release=self.go_to_modify_project)
        self.delete_project_button.bind(on_release=self.delete_project)
        self.project_list_button.bind(on_release=self.go_to_project_list)
        self.project_search_button.bind(on_release=self.go_to_project_search)

    def set_user(self, user):
        self.user = user
        if self.user.role != "admin":
            self.create_user_button.disabled = True
            self.modify_user_button.disabled = True
            self.delete_user_button.disabled = True

    def go_to_create_user(self, instance):
        self.manager.current = "user"

    def go_to_modify_user(self, instance):
        self.manager.current = "modify_user"

    def delete_user(self, instance):
        username_input = TextInput(hint_text="Username", multiline=False)
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_layout.add_widget(username_input)
        popup_layout.add_widget(
            Button(
                text="Delete",
                on_release=lambda x: self.confirm_delete_user(username_input.text),
            )
        )
        popup = Popup(title="Delete User", content=popup_layout, size_hint=(0.75, 0.5))
        popup.open()

    def confirm_delete_user(self, username):
        self.user_controller.delete_user(username)
        Popup(
            title="Success",
            content=Label(text="User deleted successfully"),
            size_hint=(0.75, 0.5),
        ).open()

    def go_to_create_project(self, instance):
        self.manager.current = "project"

    def go_to_modify_project(self, instance):
        self.manager.current = "modify_project"

    def delete_project(self, instance):
        project_name_input = TextInput(hint_text="Project Name", multiline=False)
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_layout.add_widget(project_name_input)
        popup_layout.add_widget(
            Button(
                text="Delete",
                on_release=lambda x: self.confirm_delete_project(
                    project_name_input.text
                ),
            )
        )
        popup = Popup(
            title="Delete Project", content=popup_layout, size_hint=(0.75, 0.5)
        )
        popup.open()

    def confirm_delete_project(self, project_name):
        self.project_controller.delete_project(project_name)
        Popup(
            title="Success",
            content=Label(text="Project deleted successfully"),
            size_hint=(0.75, 0.5),
        ).open()

    def go_to_project_list(self, instance):
        self.manager.current = "project_list"

    def go_to_project_search(self, instance):
        self.manager.current = "project_search"
