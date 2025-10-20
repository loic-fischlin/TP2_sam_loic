import sys
import traceback

from PyQt6.QtWidgets import QApplication
from fenetre_principale import FonctionView

if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)

    sys.excepthook = qt_exception_hook
    app = QApplication(sys.argv)
    fenetre = FonctionView()
    fenetre.show()
    sys.exit(app.exec())