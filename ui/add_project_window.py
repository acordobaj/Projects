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
from database import projects_collection
from datetime import datetime


class AddProjectWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Referencia a la ventana principal
        self.setWindowTitle("Alta de Proyectos")
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
        title_label = QLabel("Alta de Proyectos")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title_label)
        # Campo Nombre
        self.name_label = QLabel("Nombre del Proyecto:")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese el nombre del proyecto")
        layout.addWidget(self.name_input)
        # Campo Descripción
        self.description_label = QLabel("Descripción:")
        layout.addWidget(self.description_label)
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Ingrese una descripción")
        layout.addWidget(self.description_input)
        # Campo Estado (Status)
        self.status_label = QLabel("Estado del Proyecto:")
        layout.addWidget(self.status_label)
        self.status_combo = QComboBox()
        self.status_combo.addItems(
            ["En Proceso", "Terminado"]
        )  # Opciones para el estado
        layout.addWidget(self.status_combo)
        # Botón Guardar
        self.save_button = QPushButton("Guardar Proyecto")
        self.save_button.clicked.connect(self.save_project)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_project(self):
        # Obtener los valores ingresados
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()
        status = self.status_combo.currentText()  # Obtener el estado seleccionado

        if not name or not description:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Calcular el consecutivo basado en el número de proyectos existentes
        consecutive = projects_collection.count_documents({}) + 1

        # Crear el nuevo proyecto
        new_project = {
            "name": name,
            "description": description,
            "files": "Sin archivo",  # Guardar "Sin archivo" por defecto
            "status": status,  # Guardar el estado seleccionado
            "created_at": datetime.now(),
            "consecutive": consecutive,  # Agregar el campo "consecutive"
        }

        # Guardar en la base de datos
        projects_collection.insert_one(new_project)

        # Mostrar mensaje de éxito
        QMessageBox.information(self, "Éxito", f"Proyecto '{name}' guardado con éxito.")

        # Refrescar la tabla de proyectos en la ventana principal
        self.main_window.show_projects()

        # Cerrar la ventana de alta de proyectos
        self.close()
