import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show_login_window()  # Mostrar la ventana de login al inicio
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
