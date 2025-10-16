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
        loadUi("ui/function_view2.ui", self)

        self.model = FonctionModel()
        self.canvas = MPLCanvas(self.model)
        self.canvas_layout.addWidget(self.canvas)
        self.calculerPushButton.clicked.connect(self.calculer_edit)

        self.borneInfLineEdit.editingFinished.connect(self.fonction_edit)
        self.borneSupLineEdit.editingFinished.connect(self.fonction_edit)
        self.fonctionLineEdit.editingFinished.connect(self.fonction_edit)

        self.integraleLineEdit.setEnabled(False)
        self.sommeLineEdit.setEnabled(False)

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
        fonct_str = self.fonctionLineEdit.text()
        if self.model.validate_fonction(fonct_str):
            self.model.fonction = fonct_str
            self.model.borne_inf = self.borneInfLineEdit.text() or 0.0
            self.model.borne_sup = self.borneSupLineEdit.text() or 10.0
            self.nombreSlider.setMinimum(10)
            self.nombreSlider.setMaximum(100)
            self.canvas.dessiner()

        else :
            QMessageBox.critical(self, "Erreur", "La fonction est invalide")
            self.fonctionLineEdit.clear()


