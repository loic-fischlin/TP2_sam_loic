from PyQt6.QtCore import QObject, pyqtSignal
import sympy as sp


class FonctionModel(QObject):
    __x = sp.symbols("x")
    __fonction: None = None
    __borne_inf : int = 0
    __borne_sup : int = 10
    __est_droite : bool = False
    __valeur_somme : float = 0
    __valeur_integrale : float = 0

    modelChanged = pyqtSignal()

    def __init(self):
        super().__init__()

    @property
    def fonction(self):
        try:
            f = sp.lambdify(self.__x, self.__fonction, "numpy")
        except  Exception as e:
            print(e)
            f=None
        return f

    @fonction.setter
    def fonction(self, value):
        self.__fonction = sp.sympify(value)

    @property
    def borne_inf(self):
        return self.__borne_inf

    @borne_inf.setter
    def borne_inf(self, value):
        self.__borne_inf = value
        self.modelChanged.emit()

    @property
    def borne_sup(self):
        return self.__borne_sup

    @borne_sup.setter
    def borne_sup(self, value):
        self.__borne_sup = value
        self.modelChanged.emit()





