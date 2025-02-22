from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()  # No se pasa ningún argumento adicional
    login_window.show()
    sys.exit(app.exec_())
