from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from controllers.user_controller import UserController


class UserListWindow(QWidget):
    def __init__(self, main_window, current_user):
        super().__init__()
        self.main_window = main_window
        self.user_controller = UserController()
        self.current_user = current_user
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Lista de Usuarios")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 128))  # Azul
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # Blanco
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout()

        label = QLabel("Lista de Usuarios", self)
        label.setFont(QFont("Arial", 20))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Añadimos un espaciador para bajar la tabla un poco
        layout.addSpacerItem(
            QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )

        self.user_table = QTableWidget(self)
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(
            ["Nombre de Usuario", "Contraseña", "Rol", "Acciones"]
        )
        self.user_table.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )

        header = self.user_table.horizontalHeader()
        header.setStyleSheet(
            "::section { background-color: #000080; color: white; padding: 5px; }"
        )
        header.setFont(QFont("Arial", 10, QFont.Bold))
        header.setSectionResizeMode(
            QHeaderView.Stretch
        )  # Para hacer que los encabezados se ajusten al contenido

        layout.addWidget(self.user_table)
        self.setLayout(layout)

        self.refresh_user_list()

    def refresh_user_list(self):
        users = self.user_controller.get_users()
        self.update_user_table(users)

    def update_user_table(self, users):
        self.user_table.setRowCount(len(users))

        for row, user in enumerate(users):
            self.user_table.setItem(row, 0, QTableWidgetItem(user.username))
            self.user_table.setItem(row, 1, QTableWidgetItem(user.password))
            self.user_table.setItem(row, 2, QTableWidgetItem(user.role))

            if self.current_user.role in ["Media", "Admin"]:
                delete_button = QPushButton("Eliminar")
                delete_button.setStyleSheet("background-color: red; color: white;")
                delete_button.clicked.connect(
                    lambda chk, username=user.username: self.delete_user(username)
                )
                self.user_table.setCellWidget(row, 3, delete_button)

    def delete_user(self, username):
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar el usuario '{username}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.user_controller.delete_user(username)
            self.refresh_user_list()
