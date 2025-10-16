from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QDockWidget, QPushButton, QLineEdit, QMessageBox, QListView, QComboBox
from PyQt6.uic import loadUi
from fonction_integre import FonctionModel
from liste_fonctions import ListeFonctionsModel


class ListeFonctionView(QDockWidget):
    ajouterPushButton : QPushButton
    fonctionLineEditDock : QLineEdit
    listViewFonctions : QListView
    fonctionComboBox: QComboBox

    __listeModele : ListeFonctionsModel
    liste_modifiee = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi("ui/function_view2.ui", self)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        self.__listeModele = ListeFonctionsModel()

        self.ajouterPushButton.clicked.connect(self.ajouter_fonction)

        self.fonctionComboBox.setModel(self.__listeModele)
        self.listViewFonctions.setModel(self.__listeModele)

    def ajouter_fonction(self):
        texte = self.fonctionLineEditDock.text()
        if not texte:
            QMessageBox.critical(self, "Erreur", "Veuillez saisir une fonction")
            return

        test_modele = FonctionModel()
        if test_modele.validate_fonction(texte):
            self.__listeModele.add_item(texte)
            self.liste_modifiee.emit()
            self.fonctionLineEditDock.clear()
        else:
            QMessageBox.critical(self, "Erreur", "Veuillez rentrez une fonction valide")




