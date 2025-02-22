from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.main_window import MainWindow
from database import users_collection, update_project_files  # Importamos el método


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.setGeometry(300, 300, 400, 250)
        self.setFixedSize(400, 250)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #f9f9f9;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px;
                background-color: #28a745; /* Verde */
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #218838; /* Verde más oscuro */
            }
        """
        )

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title_label = QLabel("Iniciar Sesión")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title_label)

        # Campo Nombre de Usuario
        self.username_label = QLabel("Nombre de Usuario:")
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su nombre de usuario")
        layout.addWidget(self.username_input)

        # Campo Contraseña
        self.password_label = QLabel("Contraseña:")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        layout.addWidget(self.password_input)

        # Botón Iniciar Sesión
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        try:
            print(
                f"Intentando iniciar sesión con: username={username}, password={password}"
            )

            # Verificar credenciales en la base de datos
            user = users_collection.find_one(
                {"username": username, "password": password}
            )
            if not user:
                print("Usuario no encontrado en la base de datos.")
                QMessageBox.warning(self, "Error", "Credenciales incorrectas.")
                return

            print("Usuario encontrado:", user)

            # Actualizar archivos en la base de datos
            update_project_files()  # Llamamos al método desde database.py

            # Abrir la ventana principal
            self.main_window = MainWindow()
            self.main_window.set_user_role(user.get("role", "consulta"))
            self.main_window.show()
            self.close()
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            QMessageBox.critical(
                self, "Error", f"No se pudo conectar a la base de datos: {e}"
            )
