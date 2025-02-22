import os
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLabel,
    QHeaderView,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import projects_collection, users_collection
from datetime import datetime
from ui.add_project_window import AddProjectWindow
from ui.user_list_window import UserListWindow
from ui.add_user_window import AddUserWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Proyectos")
        self.setGeometry(100, 100, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f9f9f9;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
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
            QPushButton#open_button {
                background-color: #007bff;
                color: white;
            }
            QPushButton#open_button:hover {
                background-color: #0056b3;
            }
            QPushButton#delete_button {
                background-color: #dc3545;
                color: white;
            }
            QPushButton#delete_button:hover {
                background-color: #a71d2a;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """
        )

        self.role = None  # Rol del usuario actual
        self.init_ui()

    def init_ui(self):
        # Menú
        menubar = self.menuBar()
        projects_menu = menubar.addMenu("Proyectos")
        users_menu = menubar.addMenu("Usuarios")
        session_menu = menubar.addMenu(
            "Sesión"
        )  # Nuevo menú para Salir y Cerrar Sesión

        # Submenús de Proyectos
        self.list_projects_action = QAction("Lista de Proyectos", self)
        self.list_projects_action.triggered.connect(self.show_projects)
        projects_menu.addAction(self.list_projects_action)

        self.add_project_action = QAction("Alta de Proyectos", self)
        self.add_project_action.triggered.connect(self.open_add_project_window)
        projects_menu.addAction(self.add_project_action)

        # Submenús de Usuarios
        self.list_users_action = QAction("Lista de Usuarios", self)
        self.list_users_action.triggered.connect(self.open_user_list_window)
        users_menu.addAction(self.list_users_action)

        self.add_user_action = QAction("Alta de Usuarios", self)
        self.add_user_action.triggered.connect(self.open_add_user_window)
        users_menu.addAction(self.add_user_action)

        # Botón Salir
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)  # Cierra la aplicación
        session_menu.addAction(exit_action)

        # Encabezado
        header = QLabel("Lista de Proyectos")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 24, QFont.Bold))

        # Filtros
        filters_layout = QHBoxLayout()

        # Filtro por Nombre
        self.name_filter_label = QLabel("Filtrar por Nombre:")
        filters_layout.addWidget(self.name_filter_label)
        self.name_filter_input = QLineEdit()
        self.name_filter_input.setPlaceholderText("Ingrese el nombre del proyecto")
        filters_layout.addWidget(self.name_filter_input)

        # Filtro por Mes de Alta
        self.month_filter_label = QLabel("Filtrar por Mes:")
        filters_layout.addWidget(self.month_filter_label)
        self.month_filter_combo = QComboBox()
        self.month_filter_combo.addItem("Todos")
        self.month_filter_combo.addItems(
            [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Septiembre",
                "Octubre",
                "Noviembre",
                "Diciembre",
            ]
        )
        filters_layout.addWidget(self.month_filter_combo)

        # Botón Aplicar Filtros
        self.apply_filters_button = QPushButton("Aplicar Filtros")
        self.apply_filters_button.clicked.connect(self.apply_filters)
        filters_layout.addWidget(self.apply_filters_button)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Nombre", "Descripción", "Archivo", "Estado", "Abrir", "Eliminar"]
        )
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setAlternatingRowColors(True)

        # Forzar el ancho de todas las columnas
        self.table.setColumnWidth(0, 150)  # Columna "Nombre"
        self.table.setColumnWidth(1, 200)  # Columna "Descripción"
        self.table.setColumnWidth(2, 100)  # Columna "Archivo"
        self.table.setColumnWidth(3, 100)  # Columna "Estado"
        self.table.setColumnWidth(4, 80)  # Columna "Abrir"
        self.table.setColumnWidth(5, 80)  # Columna "Eliminar"

        # Desactivar el ajuste automático de todas las columnas
        for i in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Fixed)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addLayout(filters_layout)  # Agregar los filtros
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Mostrar proyectos al cargar la ventana
        self.show_projects()

    def set_user_role(self, role):
        self.role = role
        self.update_menu_permissions()

    def update_menu_permissions(self):
        if self.role == "consulta":
            # Solo puede ver la lista de proyectos y usuarios
            self.add_project_action.setEnabled(False)
            self.add_user_action.setEnabled(False)
        elif self.role == "media":
            # Puede agregar proyectos pero no usuarios
            self.add_project_action.setEnabled(True)
            self.add_user_action.setEnabled(False)
        elif self.role == "admin":
            # Tiene acceso completo
            self.add_project_action.setEnabled(True)
            self.add_user_action.setEnabled(True)

    def show_projects(self, name_filter="", month_filter=""):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(
            ["Nombre", "Descripción", "Archivo", "Estado", "Abrir", "Eliminar"]
        )

        # Obtener todos los proyectos
        projects = list(projects_collection.find())

        # Filtrar por nombre
        if name_filter:
            projects = [p for p in projects if name_filter.lower() in p["name"].lower()]

        # Filtrar por mes
        if month_filter and month_filter != "Todos":
            month_number = [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Septiembre",
                "Octubre",
                "Noviembre",
                "Diciembre",
            ].index(month_filter) + 1
            projects = [p for p in projects if p["created_at"].month == month_number]

        # Verificar archivos en la carpeta project_files
        project_files_folder = "project_files"  # Carpeta en la raíz del proyecto
        if not os.path.exists(project_files_folder):
            os.makedirs(project_files_folder)

        for project in projects:
            # Verificar si existe un archivo con el consecutivo del proyecto
            consecutive = str(project.get("consecutive", ""))
            file_name = f"{consecutive}_proyecto.pdf"  # Formato esperado del archivo
            file_path = os.path.join(project_files_folder, file_name)

            if os.path.exists(file_path):
                # Actualizar el campo "files" en la base de datos si existe el archivo
                if project.get("files", "Sin archivo") != file_name:
                    projects_collection.update_one(
                        {"_id": project["_id"]}, {"$set": {"files": file_name}}
                    )
                    project["files"] = file_name  # Actualizar el proyecto localmente
            else:
                # Si no existe el archivo, asegurarse de que el campo "files" sea "Sin archivo"
                if project.get("files", "") != "Sin archivo":
                    projects_collection.update_one(
                        {"_id": project["_id"]}, {"$set": {"files": "Sin archivo"}}
                    )
                    project["files"] = "Sin archivo"

        # Mostrar los proyectos filtrados
        for project in projects:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Nombre
            self.table.setItem(row_position, 0, QTableWidgetItem(project["name"]))

            # Descripción
            self.table.setItem(
                row_position, 1, QTableWidgetItem(project["description"])
            )

            # Archivo
            file_name = project.get(
                "files", "Sin archivo"
            )  # Si no hay archivo, mostrar "Sin archivo"
            self.table.setItem(row_position, 2, QTableWidgetItem(file_name))

            # Estado
            status = project.get(
                "status", "En Proceso"
            )  # Si no hay estado, mostrar "En Proceso" por defecto
            self.table.setItem(row_position, 3, QTableWidgetItem(status))

            # Botón Abrir (solo si hay un archivo adjunto)
            if file_name and file_name != "Sin archivo":
                file_path = os.path.join("project_files", file_name)
                open_button = QPushButton("Abrir")
                open_button.setObjectName("open_button")
                open_button.setFixedSize(80, 30)
                open_button.clicked.connect(
                    lambda _, path=file_path: self.open_file(path)
                )
                self.table.setCellWidget(row_position, 4, open_button)
            else:
                # Si no hay archivo, dejar la celda vacía
                self.table.setItem(row_position, 4, QTableWidgetItem(""))

            # Botón Eliminar
            delete_button = QPushButton("Eliminar")
            delete_button.setObjectName("delete_button")
            delete_button.setFixedSize(80, 30)
            delete_button.clicked.connect(
                lambda _, id=project["_id"]: self.delete_project(id)
            )
            self.table.setCellWidget(row_position, 5, delete_button)

    def apply_filters(self):
        # Obtener los valores de los filtros
        name_filter = self.name_filter_input.text().strip()
        month_filter = self.month_filter_combo.currentText()

        # Actualizar la tabla con los filtros aplicados
        self.show_projects(name_filter=name_filter, month_filter=month_filter)

    def open_file(self, file_path):
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(self, "Error", "El archivo no existe.")

    def delete_project(self, project_id):
        reply = QMessageBox.question(
            self,
            "Confirmación",
            "¿Está seguro de que desea eliminar este proyecto?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            projects_collection.delete_one({"_id": project_id})
            QMessageBox.information(self, "Éxito", "Proyecto eliminado.")
            self.show_projects()

    def open_add_project_window(self):
        self.add_project_window = AddProjectWindow(
            self
        )  # Pasar referencia de MainWindow
        self.add_project_window.show()

    def open_user_list_window(self):
        self.user_list_window = UserListWindow()
        self.user_list_window.show()

    def open_add_user_window(self):
        self.add_user_window = AddUserWindow()
        self.add_user_window.show()

    def closeEvent(self, event):
        # Sobrescribir el evento de cierre para cerrar la aplicación completamente
        reply = QMessageBox.question(
            self,
            "Confirmación",
            "¿Está seguro de que desea salir de la aplicación?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
