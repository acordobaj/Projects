from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from views.login_window import LoginWindow
from views.main_window import MainWindow
from views.user_window import UserWindow
from views.modify_user_window import ModifyUserWindow
from views.project_window import ProjectWindow
from views.modify_project_window import ModifyProjectWindow
from views.project_list_window import ProjectListWindow
from views.project_search_window import ProjectSearchWindow


class ProjectManagementApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.login_screen = LoginWindow(name="login")
        self.main_screen = MainWindow(name="main")
        self.user_screen = UserWindow(name="user")
        self.modify_user_screen = ModifyUserWindow(name="modify_user")
        self.project_screen = ProjectWindow(name="project")
        self.modify_project_screen = ModifyProjectWindow(name="modify_project")
        self.project_list_screen = ProjectListWindow(name="project_list")
        self.project_search_screen = ProjectSearchWindow(name="project_search")

        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.user_screen)
        self.screen_manager.add_widget(self.modify_user_screen)
        self.screen_manager.add_widget(self.project_screen)
        self.screen_manager.add_widget(self.modify_project_screen)
        self.screen_manager.add_widget(self.project_list_screen)
        self.screen_manager.add_widget(self.project_search_screen)

        self.screen_manager.current = "login"  # Start with the login screen
        return self.screen_manager


if __name__ == "__main__":
    ProjectManagementApp().run()
