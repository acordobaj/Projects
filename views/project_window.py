from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QMessageBox,
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from controllers.project_controller import ProjectController


class ProjectWindow(QWidget):
    def __init__(self, main_window, current_user):
        super().__init__()
        self.main_window = main_window
        self.project_controller = ProjectController()
        self.current_user = current_user
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Crear Proyecto")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 128))  # Azul
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # Blanco
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout()

        label = QLabel("Crear Proyecto", self)
        label.setFont(QFont("Arial", 20))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nombre del Proyecto")
        self.name_input.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        layout.addWidget(self.name_input)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Descripción del Proyecto")
        self.description_input.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        layout.addWidget(self.description_input)

        self.status_input = QComboBox(self)
        self.status_input.addItem("En Proceso")
        self.status_input.addItem("Terminado")
        self.status_input.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        layout.addWidget(self.status_input)

        button = QPushButton("Crear Proyecto", self)
        button.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        button.clicked.connect(self.create_project)
        layout.addWidget(button)

        self.setLayout(layout)

    def create_project(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        status = self.status_input.currentText()

        if name and description:
            self.project_controller.create_project(name, description, status)
            QMessageBox.information(self, "Éxito", "Proyecto creado exitosamente")
            self.main_window.project_list_screen.refresh_project_list()
            self.main_window.switch_screen(self.main_window.project_list_screen)
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
