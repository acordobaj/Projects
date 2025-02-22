from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QHeaderView,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import users_collection


class UserListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Usuarios")
        self.setGeometry(200, 200, 800, 600)  # Tamaño de la ventana
        self.setFixedSize(800, 600)  # Evitar que se redimensione
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f9f9f9;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QTableWidget {
                gridline-color: #ccc;
                font-size: 14px;
            }
            QPushButton {
                padding: 0px;
                margin: 0px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 80px;
                max-width: 80px;
                min-height: 30px;
                max-height: 30px;
            }
            QPushButton#delete_button {
                background-color: #dc3545; /* Rojo */
                color: white;
            }
            QPushButton#delete_button:hover {
                background-color: #a71d2a; /* Rojo más oscuro al pasar el mouse */
            }
        """
        )

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Encabezado
        header = QLabel("Lista de Usuarios")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(header)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Usuario", "Rol", "Contraseña", "Eliminar"]
        )
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setAlternatingRowColors(True)

        # Forzar el ancho de las columnas
        self.table.setColumnWidth(0, 200)  # Columna "Usuario"
        self.table.setColumnWidth(1, 150)  # Columna "Rol"
        self.table.setColumnWidth(2, 200)  # Columna "Contraseña"
        self.table.setColumnWidth(3, 80)  # Columna "Eliminar"

        # Desactivar el ajuste automático de todas las columnas
        for i in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Fixed)

        layout.addWidget(self.table)
        self.setLayout(layout)

        # Mostrar usuarios al cargar la ventana
        self.show_users()

    def show_users(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(
            ["Usuario", "Rol", "Contraseña", "Eliminar"]
        )

        users = list(users_collection.find())
        for user in users:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Usuario (username)
            username = user.get(
                "username", "Sin nombre"
            )  # Usar "Sin nombre" si el campo no existe
            self.table.setItem(row_position, 0, QTableWidgetItem(username))

            # Rol
            role = user.get("role", "Sin rol")  # Usar "Sin rol" si el campo no existe
            self.table.setItem(row_position, 1, QTableWidgetItem(role))

            # Contraseña
            password = user.get(
                "password", "Sin contraseña"
            )  # Usar "Sin contraseña" si el campo no existe
            self.table.setItem(row_position, 2, QTableWidgetItem(password))

            # Botón Eliminar
            delete_button = QPushButton("Eliminar")
            delete_button.setObjectName("delete_button")
            delete_button.setFixedSize(80, 30)
            delete_button.clicked.connect(
                lambda _, id=user["_id"]: self.delete_user(id)
            )
            self.table.setCellWidget(row_position, 3, delete_button)

    def delete_user(self, user_id):
        reply = QMessageBox.question(
            self,
            "Confirmación",
            "¿Está seguro de que desea eliminar este usuario?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            users_collection.delete_one({"_id": user_id})
            QMessageBox.information(self, "Éxito", "Usuario eliminado.")
            self.show_users()
