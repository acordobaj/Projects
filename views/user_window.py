from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from controllers.user_controller import UserController


class UserWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_controller = UserController()

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(
            hint_text="Password", password=True, multiline=False
        )
        self.role_input = Spinner(
            text="Select Role", values=("basic", "media", "admin")
        )
        self.create_button = Button(text="Create User", on_release=self.create_user)
        self.back_button = Button(text="Back", on_release=self.go_back)

        layout.add_widget(Label(text="Create User"))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.role_input)
        layout.add_widget(self.create_button)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def create_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        role = self.role_input.text
        self.user_controller.create_user(username, password, role)
        Popup(
            title="Success",
            content=Label(text="User created successfully"),
            size_hint=(0.75, 0.5),
        ).open()
        self.manager.current = "main"

    def go_back(self, instance):
        self.manager.current = "main"
