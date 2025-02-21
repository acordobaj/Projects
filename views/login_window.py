from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from controllers.user_controller import UserController


class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.user_controller = UserController()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Inicio de Sesión")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 128))  # Azul
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # Blanco
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout()

        label = QLabel("Inicio de Sesión", self)
        label.setFont(QFont("Arial", 20))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nombre de Usuario")
        self.username_input.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        layout.addWidget(self.password_input)

        login_button = QPushButton("Iniciar Sesión", self)
        login_button.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.user_controller.login(username, password)

        if user:
            self.main_window.current_user = user
            self.main_window.show_main_window()
            self.close()
        else:
            QMessageBox.warning(
                self, "Error", "Nombre de usuario o contraseña incorrectos"
            )
