from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QComboBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import users_collection


class AddUserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alta de Usuarios")
        self.setGeometry(200, 200, 400, 350)  # Tamaño de la ventana
        self.setFixedSize(400, 350)  # Evitar que se redimensione
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
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """
        )

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title_label = QLabel("Alta de Usuarios")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title_label)

        # Campo Usuario
        self.username_label = QLabel("Usuario:")
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese el nombre de usuario")
        layout.addWidget(self.username_input)

        # Campo Contraseña
        self.password_label = QLabel("Contraseña:")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese la contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)  # Ocultar contraseña
        layout.addWidget(self.password_input)

        # Campo Rol
        self.role_label = QLabel("Rol:")
        layout.addWidget(self.role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Consulta", "Media", "Admin"])  # Opciones de rol
        layout.addWidget(self.role_combo)

        # Botón Guardar
        self.save_button = QPushButton("Guardar Usuario")
        self.save_button.clicked.connect(self.save_user)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_user(self):
        # Obtener los valores ingresados
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText().lower()  # Convertir a minúsculas

        if not username or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Verificar si el usuario ya existe
        if users_collection.find_one({"username": username}):
            QMessageBox.warning(self, "Error", "El nombre de usuario ya está en uso.")
            return

        # Crear el nuevo usuario
        new_user = {"username": username, "password": password, "role": role}

        # Guardar en la base de datos
        users_collection.insert_one(new_user)

        # Mostrar mensaje de éxito
        QMessageBox.information(
            self, "Éxito", f"Usuario '{username}' guardado con éxito."
        )

        # Limpiar los campos
        self.username_input.clear()
        self.password_input.clear()
