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

                borne_inf = self.__model.borne_inf
                borne_sup = self.__model.borne_sup

                if borne_inf >= borne_sup:
                    QMessageBox.critical(self, "Erreur", "La borne inférieure doit être plus petite que la borne supérieure.")
                    return

                x = np.linspace(borne_inf, borne_sup, 1000)
                y = f(x)
                self.__ax.plot(x, y)

            self.draw()

        except ValueError:
            QMessageBox.critical(self, "Erreur", "Les bornes doivent être des nombres valides.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"La fonction n'est pas valide :\n{e}")

