import os.path
import subprocess
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QDockWidget, QPushButton, QLineEdit, QMessageBox, QListView
from PyQt6.uic import loadUi
from fonction_integre import FonctionModel
from liste_fonctions import ListeFonctionsModel


class ListeFonctionView(QDockWidget):
    ajouterPushButton: QPushButton
    supprimerPushButton: QPushButton
    enregistrerPushButton: QPushButton
    fonctionLineEditDock: QLineEdit
    listViewFonctions: QListView

    __listeModele: ListeFonctionsModel
    liste_modifiee = pyqtSignal()

    def __init__(self, modele_partage):
        super().__init__()
        loadUi("ui/dockwidget.ui", self)
        self.setWindowTitle("Liste des fonctions")
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)

        self.__listeModele = modele_partage
        self.listViewFonctions.setModel(self.__listeModele)

        self.ajouterPushButton.setEnabled(False)
        self.activer_bouton_supprimer()
        self.fonctionLineEditDock.textChanged.connect(self.activer_bouton_ajouter)
        self.listViewFonctions.selectionModel().selectionChanged.connect(self.activer_bouton_supprimer)

        self.ajouterPushButton.clicked.connect(self.ajouter_fonction)
        self.supprimerPushButton.clicked.connect(self.supprimer_fonction)
        self.enregistrerPushButton.clicked.connect(self.enregistrer_donnees)

    def enregistrer_donnees(self):
        try:
            chemin_fichier = "json/fonctions.json"

            self.__listeModele.save_to_json(chemin_fichier)

            QMessageBox.information(self, "Succès", "Fichier 'fonctions.json' enregistré avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d’enregistrer le fichier : {str(e)}")

    def activer_bouton_ajouter(self):
        if self.fonctionLineEditDock.text():
            self.ajouterPushButton.setEnabled(True)

    def activer_bouton_supprimer(self):
        if self.listViewFonctions.currentIndex().isValid():
            self.supprimerPushButton.setEnabled(True)
        else:
            self.supprimerPushButton.setEnabled(False)

    def ajouter_fonction(self):
        texte = self.fonctionLineEditDock.text()
        test_modele = FonctionModel()
        if test_modele.validate_fonction(texte):
            self.__listeModele.add_item(texte)
            self.fonctionLineEditDock.clear()
            self.ajouterPushButton.setEnabled(False)
        else:
            QMessageBox.critical(self, "Erreur", "Veuillez rentrez une fonction valide")

    def supprimer_fonction(self):
        fonctionSupp = self.listViewFonctions.currentIndex()
        self.__listeModele.remove_item(fonctionSupp.row())
        self.activer_bouton_supprimer()


    def closeEvent(self, event):
        event.ignore()
        self.hide()
