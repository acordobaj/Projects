from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from controllers.user_controller import UserController


class UserWindow(QWidget):
    def __init__(self, main_window, current_user):
        super().__init__()
        self.main_window = main_window
        self.current_user = current_user
        self.user_controller = UserController()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Crear Usuario")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 128))  # Azul
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # Blanco
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout()

        label = QLabel("Crear Usuario", self)
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

        self.role_input = QComboBox(self)
        self.role_input.addItems(["Básica", "Media", "Admin"])
        self.role_input.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        layout.addWidget(self.role_input)

        create_button = QPushButton("Crear Usuario", self)
        create_button.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        create_button.clicked.connect(self.create_user)
        layout.addWidget(create_button)

        self.setLayout(layout)

    def create_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()

        if username and password:
            self.user_controller.create_user(username, password, role)
            QMessageBox.information(self, "Éxito", "Usuario creado exitosamente")
            self.main_window.switch_screen(self.main_window.user_list_screen)
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
