import sys

from PyQt6.QtWidgets import QApplication
import fenetre_principale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FonctionView()
    fenetre.show()
    sys.exit(app.exec())