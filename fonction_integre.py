import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal
import sympy as sp


class FonctionModel(QObject):
    __x = sp.symbols("x")
    __fonction: None = None
    __borne_inf: float = 0.0
    __borne_sup: float = 10.0
    __est_droite: bool = False
    __valeur_somme: float = 0
    __valeur_integrale: float = 0

    modelChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

    @property
    def fonction(self):
        try:
            f = sp.lambdify(self.__x, self.__fonction, "numpy")
        except  Exception as e:
            print(e)
            f = None
        return f

    @fonction.setter
    def fonction(self, value):
        self.__fonction = sp.sympify(value)
        self.modelChanged.emit()

    @property
    def est_droite(self):
        return self.__est_droite

    @est_droite.setter
    def est_droite (self, value):
        self.__est_droite = bool(value)
        self.modelChanged.emit()

    @property
    def borne_inf(self):
        return self.__borne_inf

    @borne_inf.setter
    def borne_inf(self, value):
        if self.validate_borne(value):
            self.__borne_inf = float(value)
            self.modelChanged.emit()
        else:
            print(f"Borne inférieure invalide : {value}")

    @property
    def borne_sup(self):
        return self.__borne_sup

    @borne_sup.setter
    def borne_sup(self, value):
        if self.validate_borne(value):
            self.__borne_sup = float(value)
            self.modelChanged.emit()
        else:
            print(f"Borne supérieure invalide : {value}")

    @property
    def variable(self):
        return self.__x

    def validate_fonction(self, f_str):
        try:
            expr = sp.sympify(f_str)
            if expr.free_symbols != {self.__x}:
                print("La fonction ne doit contenir qu'une seule variable x.")
                return False
            sp.lambdify(self.__x, expr, "numpy")
            return True
        except Exception as e:
            print(f"Erreur lors de la validation de la fonction : {e}")
            return False

    def validate_borne(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @property
    def valeur_integrale(self):
        return self.__valeur_integrale

    def calculer_integrale(self):
        try:
            self.__valeur_integrale = float(
                sp.integrate(self.__fonction, (self.__x, self.__borne_inf, self.__borne_sup))
            )
        except Exception as e:
            print(f"Erreur calcul intégrale : {e}")
            self.__valeur_integrale = 0
        self.modelChanged.emit()
        return self.__valeur_integrale

    @property
    def valeur_somme(self):
        return self.__valeur_somme

    def calculer_somme(self, n):

        f_num = sp.lambdify(self.__x, self.__fonction, "numpy")

        a, b = self.__borne_inf, self.__borne_sup
        n = int(n)
        dx = (b-a) / n

        # calcule des points cherché sur chatGPT
        if self.est_droite:
            xs = np.linspace(a, b - dx, n)
        else :
            xs = np.linspace(a + dx, b, n)

        ys = f_num(xs)
        somme = float(np.sum(ys * dx))
        self.modelChanged.emit()
        return somme, xs, ys, dx


