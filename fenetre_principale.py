from PyQt6.QtWidgets import QMainWindow, QLineEdit, QSlider, QVBoxLayout, QRadioButton, QPushButton, QMessageBox
from fonction_integre import FonctionModel
from PyQt6.uic import loadUi

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

    __model : FonctionModel

    def __init__(self):
        super().__init__()
        loadUi("ui/function_view.ui", self)

        self.model = FonctionModel()
        canvas = MPLCanvas(self.model)
        self.canvas_layout.addWidget(canvas)

        self.borneInfLineEdit.editingFinished.connect()
        self.fonctionLineEdit.editingFinished.connect(self.fonction_edit)
        self.fonctionLineEdit.editingFinished.connect(canvas.dessiner)


    def fonction_edit(self):
        fonct_str = self.fonctionLineEdit.text()
        if self.model.validate_fonction(fonct_str) :
            self.model.fonction = fonct_str
            #attribuer les bornes

        else :
            QMessageBox.critical(self, "Erreur", "La fonction est invalide")
            self.fonctionLineEdit.clear()


