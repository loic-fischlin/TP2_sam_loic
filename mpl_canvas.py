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
                borne_inf_text = str(self.__model.borne_inf).strip()
                borne_sup_text = str(self.__model.borne_sup).strip()

                borne_inf = float(borne_inf_text) if borne_inf_text else 0.0
                borne_sup = float(borne_sup_text) if borne_sup_text else 10.0

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

