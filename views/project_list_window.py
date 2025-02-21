from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QHBoxLayout,
    QHeaderView,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from controllers.project_controller import ProjectController
import os


class ProjectListWindow(QWidget):
    def __init__(self, main_window, current_user):
        super().__init__()
        self.main_window = main_window
        self.project_controller = ProjectController()
        self.current_user = current_user
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Lista de Proyectos")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 128))  # Azul
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # Blanco
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout()

        label = QLabel("Lista de Proyectos", self)
        label.setFont(QFont("Arial", 20))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Añadimos un espaciador para bajar la tabla un poco
        layout.addSpacerItem(
            QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )

        # Filtros de búsqueda
        filter_layout = QHBoxLayout()
        self.name_filter_input = QLineEdit(self)
        self.name_filter_input.setPlaceholderText("Buscar por nombre de proyecto")
        self.name_filter_input.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        filter_layout.addWidget(self.name_filter_input)

        self.month_filter_input = QComboBox(self)
        self.month_filter_input.addItem("Seleccionar mes de alta")
        for month in range(1, 13):
            self.month_filter_input.addItem(str(month))
        self.month_filter_input.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        filter_layout.addWidget(self.month_filter_input)

        filter_button = QPushButton("Aplicar Filtros", self)
        filter_button.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )
        filter_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(filter_button)

        layout.addLayout(filter_layout)

        self.project_table = QTableWidget(self)
        self.project_table.setColumnCount(7)
        self.project_table.setHorizontalHeaderLabels(
            [
                "Consecutivo",
                "Nombre",
                "Descripción",
                "Archivo(s)",
                "Estatus",
                "Abrir Archivo",
                "Acciones",
            ]
        )
        self.project_table.setStyleSheet(
            "background-color: white; color: black; margin-bottom: 10px;"
        )

        header = self.project_table.horizontalHeader()
        header.setStyleSheet(
            "::section { background-color: #000080; color: white; padding: 5px; }"
        )
        header.setFont(QFont("Arial", 10, QFont.Bold))
        header.setSectionResizeMode(
            QHeaderView.Stretch
        )  # Para hacer que los encabezados se ajusten al contenido

        layout.addWidget(self.project_table)
        self.setLayout(layout)

        self.refresh_project_list()

    def refresh_project_list(self):
        projects = self.project_controller.get_projects()
        self.update_project_table(projects)

    def apply_filters(self):
        name_filter = self.name_filter_input.text()
        month_filter = self.month_filter_input.currentText()
        month_filter = int(month_filter) if month_filter.isdigit() else None

        projects = self.project_controller.filter_projects(name_filter, month_filter)
        self.update_project_table(projects)

    def update_project_table(self, projects):
        self.project_table.setRowCount(len(projects))

        for row, project in enumerate(projects):
            self.project_table.setItem(
                row, 0, QTableWidgetItem(str(project.consecutive))
            )
            self.project_table.setItem(row, 1, QTableWidgetItem(project.name))
            self.project_table.setItem(row, 2, QTableWidgetItem(project.description))
            self.project_table.setItem(row, 3, QTableWidgetItem(project.files))
            self.project_table.setItem(row, 4, QTableWidgetItem(project.status))

            if project.files != "Sin archivo":
                button = QPushButton("Abrir")
                button.setStyleSheet(
                    "background-color: white; color: black; margin-bottom: 10px;"
                )
                button.clicked.connect(
                    lambda chk, file_path=project.files: self.open_file(file_path)
                )
                self.project_table.setCellWidget(row, 5, button)
            else:
                self.project_table.setItem(row, 5, QTableWidgetItem(""))

            if self.current_user.role in ["Media", "Admin"]:
                delete_button = QPushButton("Eliminar")
                delete_button.setStyleSheet("background-color: red; color: white;")
                delete_button.clicked.connect(
                    lambda chk, consecutive=project.consecutive: self.delete_project(
                        consecutive
                    )
                )
                self.project_table.setCellWidget(row, 6, delete_button)

    def open_file(self, file_name):
        file_path = os.path.join("project_files", file_name)
        if os.path.exists(file_path):
            os.startfile(
                file_path
            )  # Esto abrirá el archivo en su aplicación predeterminada
        else:
            QMessageBox.warning(self, "Error", "El archivo no existe")

    def delete_project(self, consecutive):
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar el proyecto con consecutivo '{consecutive}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.project_controller.delete_project(consecutive)
            self.refresh_project_list()
