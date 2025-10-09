import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtWidgets import QMessageBox
from matplotlib_inline.backend_inline import FigureCanvas


class MPLCanvas(FigureCanvas)
    __model: FonctionModel

    def __init__(self,modele: FonctionModel):
        self.__fig, self.__ax = plt.subplots()
        super().__init__(self.__fig)

        self.__model = modele
        self.__model.modeChanged.connect(self.dessiner)

    def dessiner(self):
        try :
            self.__ax.clear()
            f = self.__model.fonction
            if f :
                x = np.linespace (0, 10, 1000)
                y = f(x)

                self.__ax.plot(x,y)
            self.draw()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "La fonction n'est point valide")
