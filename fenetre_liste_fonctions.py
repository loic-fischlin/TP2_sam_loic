from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QDockWidget, QPushButton, QLineEdit, QMessageBox, QListView, QComboBox
from PyQt6.uic import loadUi
from fonction_integre import FonctionModel
from liste_fonctions import ListeFonctionsModel


class ListeFonctionView(QDockWidget):
    ajouterPushButton : QPushButton
    supprimerPushButton : QPushButton
    fonctionLineEditDock : QLineEdit
    listViewFonctions : QListView


    __listeModele : ListeFonctionsModel
    liste_modifiee = pyqtSignal()

    def __init__(self, modele_partage):
        super().__init__()
        loadUi("ui/dockwidget.ui", self)
        self.setWindowTitle("Liste des fonctions")
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)

        self.__listeModele = modele_partage

        self.ajouterPushButton.clicked.connect(self.ajouter_fonction)
        self.supprimerPushButton.clicked.connect(self.supprimer_fonction)


        self.listViewFonctions.setModel(self.__listeModele)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def ajouter_fonction(self):
        texte = self.fonctionLineEditDock.text()
        if not texte:
            QMessageBox.critical(self, "Erreur", "Veuillez saisir une fonction")
            return

        test_modele = FonctionModel()
        if test_modele.validate_fonction(texte):
            self.__listeModele.add_item(texte)
            self.fonctionLineEditDock.clear()
        else:
            QMessageBox.critical(self, "Erreur", "Veuillez rentrez une fonction valide")

    def supprimerPushButton(self):
        fonctionASup = self.listViewFonctions.currentIndex()




