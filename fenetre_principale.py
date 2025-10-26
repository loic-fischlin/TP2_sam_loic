from fileinput import filename

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QSlider, QVBoxLayout, QRadioButton, QPushButton, QMessageBox, \
    QComboBox, QMenu, QMenuBar, QFileDialog

from fenetre_liste_fonctions import ListeFonctionView
from fonction_integre import FonctionModel
from PyQt6.uic import loadUi

from liste_fonctions import ListeFonctionsModel
from mpl_canvas import MPLCanvas



class FonctionView(QMainWindow):
    fonctionLineEdit : QLineEdit
    borneInfLineEdit : QLineEdit
    borneSupLineEdit : QLineEdit
    canvas_layout : QVBoxLayout
    nombreSlider : QSlider
    gaucheRadioButton : QRadioButton
    droiteRadioButton : QRadioButton
    calculerPushButton : QPushButton
    exporterPushButton : QPushButton
    sommeLineEdit : QLineEdit
    integraleLineEdit : QLineEdit
    actionFonctions : QAction
    menuFonctions : QMenu
    menubar : QMenuBar
    fonctionComboBox : QComboBox

    __model : FonctionModel

    def __init__(self):
        super().__init__()
        loadUi("ui/function_view2.ui", self)
        try:
            with open("style.qss", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Fichier style.qss introuvable")

        self.model = FonctionModel()
        self.canvas = MPLCanvas(self.model)
        self.canvas_layout.addWidget(self.canvas)
        self.calculerPushButton.clicked.connect(self.calculer_edit)
        self.borneInfLineEdit.setPlaceholderText("0")
        self.borneSupLineEdit.setPlaceholderText("10")

        self.borneInfLineEdit.textChanged.connect(lambda: self.borneInfLineEdit.setStyleSheet("background color: grey"))
        self.borneSupLineEdit.textChanged.connect(lambda: self.borneSupLineEdit.setStyleSheet("background color: grey"))
        self.borneInfLineEdit.editingFinished.connect(self.verifier_borne_inf)
        self.borneSupLineEdit.editingFinished.connect(self.verifier_borne_sup)
        self.borneInfLineEdit.editingFinished.connect(self.fonction_edit)
        self.borneSupLineEdit.editingFinished.connect(self.fonction_edit)

        self.fonctionComboBox.currentIndexChanged.connect(self.fonction_edit)
        self.exporterPushButton.clicked.connect(self.exporter_graphique)
        self.fonctionComboBox.setIconSize(QtCore.QSize(200, 30))


        self.actionFonctions.triggered.connect(self.ouvrir_listeview)
        self.dock_widget = None

        self.__listeModele = ListeFonctionsModel().load_from_json("json/fonctions.json")
        self.fonctionComboBox.setModel(self.__listeModele)


        self.integraleLineEdit.setEnabled(False)
        self.sommeLineEdit.setEnabled(False)

    def ouvrir_listeview(self):
        if self.dock_widget is None:
            self.dock_widget = ListeFonctionView(self.__listeModele)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_widget)
        else:
            self.dock_widget.show()
            self.dock_widget.raise_()

    def calculer_edit(self):
        if self.model.fonction is None:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer une fonction valide.")
            return

        self.model.est_droite = self.droiteRadioButton.isChecked()

        integrale = self.model.calculer_integrale()
        self.integraleLineEdit.setText(str(integrale))

        somme, xs, ys, dx = self.model.calculer_somme(self.nombreSlider.value())
        self.sommeLineEdit.setText(str(somme))


        self.canvas.dessiner()
        self.canvas.dessiner_rectagles(xs, ys, dx)



    def fonction_edit(self):
        fonct_str = self.fonctionComboBox.currentData(Qt.ItemDataRole.UserRole)
        if self.model.validate_fonction(fonct_str):
            self.model.fonction = fonct_str
            self.model.borne_inf = float(self.borneInfLineEdit.text().strip() or 0.0)
            self.model.borne_sup = float(self.borneSupLineEdit.text().strip() or 10.0)
            self.nombreSlider.setMinimum(10)
            self.nombreSlider.setMaximum(100)
            self.canvas.dessiner()

    def verifier_borne_inf(self):
        texte = self.borneInfLineEdit.text().strip()
        if texte == "":
            return
        try:
            valeur = float(texte)
            self.model.borne_inf = valeur
            self.borneInfLineEdit.setStyleSheet("")
        except ValueError:
            self.borneInfLineEdit.setStyleSheet("background-color: red")
            QMessageBox.critical(self, "Erreur", f"Borne inférieure invalide : '{texte}'")

    def verifier_borne_sup(self):
        texte = self.borneSupLineEdit.text().strip()
        if texte == "":
            return
        try:
            valeur = float(texte)
            self.model.borne_sup = valeur
            self.borneSupLineEdit.setStyleSheet("")

        except ValueError:
            self.borneSupLineEdit.setStyleSheet("background-color: red")
            QMessageBox.critical(self, "Erreur", f"Borne supérieure invalide : '{texte}'")

    #fonction de chatGPT
    def exporter_graphique(self):
        filename, _ = QFileDialog.getSaveFileName( #le QFileDialog ouvre l'explorateur de fichier
            self,
            "Exporter le graphique",
            "",
            "Images PNG (*.png);;JPEG (*.jpg);;All Files (*)"
        )

        if filename:
            self.canvas.exporter_image(filename)

