from PyQt5.QtWidgets import QMainWindow, QAction, QMenuBar
from views.user_list_window import UserListWindow
from views.project_list_window import ProjectListWindow
from views.project_window import ProjectWindow
from views.login_window import LoginWindow
from views.user_window import UserWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.project_list_screen = None
        self.user_list_screen = None
        self.create_project_screen = None
        self.create_user_screen = None
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Main Window")
        self.create_menu()

    def show_login_window(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()
        self.hide()  # Oculta la ventana principal hasta que el usuario inicie sesión

    def show_main_window(self):
        self.project_list_screen = ProjectListWindow(self, self.current_user)
        self.user_list_screen = UserListWindow(self, self.current_user)
        self.create_project_screen = ProjectWindow(self, self.current_user)
        self.create_user_screen = UserWindow(self, self.current_user)
        self.switch_screen(self.project_list_screen)
        self.show()  # Muestra la ventana principal después de iniciar sesión

    def create_menu(self):
        menubar = self.menuBar()

        # Menú de Usuarios
        userMenu = menubar.addMenu("Usuarios")
        user_list_action = QAction("Lista de Usuarios", self)
        user_list_action.triggered.connect(
            lambda: self.switch_screen(self.user_list_screen)
        )
        userMenu.addAction(user_list_action)

        create_user_action = QAction("Crear Usuario", self)
        create_user_action.triggered.connect(
            lambda: self.switch_screen(self.create_user_screen)
        )
        userMenu.addAction(create_user_action)

        # Menú de Proyectos
        projectMenu = menubar.addMenu("Proyectos")
        project_list_action = QAction("Lista de Proyectos", self)
        project_list_action.triggered.connect(
            lambda: self.switch_screen(self.project_list_screen)
        )
        projectMenu.addAction(project_list_action)

        create_project_action = QAction("Crear Proyecto", self)
        create_project_action.triggered.connect(
            lambda: self.switch_screen(self.create_project_screen)
        )
        projectMenu.addAction(create_project_action)

        # Menú de Archivo
        fileMenu = menubar.addMenu("Archivo")
        logout_action = QAction("Cerrar sesión", self)
        logout_action.triggered.connect(self.logout)
        fileMenu.addAction(logout_action)

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        fileMenu.addAction(exit_action)

    def switch_screen(self, screen):
        self.setCentralWidget(screen)

    def logout(self):
        self.current_user = None
        self.show_login_window()
