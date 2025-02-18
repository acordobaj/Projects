from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from controllers.user_controller import UserController


class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_controller = UserController()

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(
            hint_text="Password", password=True, multiline=False
        )
        self.login_button = Button(text="Login", on_release=self.login)

        layout.add_widget(Label(text="Login"))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.login_button)

        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        user = self.user_controller.login(username, password)
        if user:
            self.manager.current = "main"
            self.manager.get_screen("main").set_user(user)
        else:
            self.username_input.text = ""
            self.password_input.text = ""
            self.username_input.hint_text = "Invalid credentials"
            self.password_input.hint_text = ""
