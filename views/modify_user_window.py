from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class ModifyUserWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Modificar Usuario", self)
        layout.addWidget(label)

        button = QPushButton("Volver", self)
        button.clicked.connect(self.go_back)
        layout.addWidget(button)

        self.setLayout(layout)

    def go_back(self):
        self.main_window.switch_screen(self.main_window.user_screen)
