import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtWidgets import QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from fonction_integre import FonctionModel

class MPLCanvas(FigureCanvas):
    def __init__(self, modele: FonctionModel):
        self.__fig, self.__ax = plt.subplots()
        super().__init__(self.__fig)

        self.__model = modele
        self.__model.modelChanged.connect(self.dessiner)


    def dessiner(self):
        try:
            self.__ax.clear()
            f = self.__model.fonction
            if f is not None:
                x = np.linspace(self.__model.borne_inf, self.__model.borne_sup.borne_sup, 1000)
                y = f(x)
                self.__ax.plot(x, y)
            self.draw()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"La fonction n'est pas valide :\n{e}")
