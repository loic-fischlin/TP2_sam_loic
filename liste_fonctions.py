import os
import matplotlib.pyplot as plt
from PyQt6.QtGui import QPixmap, QImage
from io import BytesIO
import json
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal

class ListeFonctionsModel(QAbstractListModel):
    dataChangedSignal = pyqtSignal()

    def __init__(self, fonctions=None):
        super().__init__()
        self.__fonctions = fonctions or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.__fonctions)

    def data(self, index, role):
        if not index.isValid():
            return None

        fonction_python = self.__fonctions[index.row()]

        if role == Qt.ItemDataRole.DecorationRole:
            latex_expr = self.python_to_latex(fonction_python)
            return self.latex_to_pixmap(latex_expr)

        elif role == Qt.ItemDataRole.ToolTipRole:
            return f"Fonction : {fonction_python}"

        elif role == Qt.ItemDataRole.UserRole:
            return fonction_python

        return None

    def python_to_latex(self, expr: str) -> str:
        """Convertit x**2 en x^2 et x*y en x·y pour un rendu manuscrit"""
        import re
        def replacer(match):
            base = match.group(1)
            exp = match.group(2)
            return f"{base}^{{{exp}}}"  # x^2 -> x^{2}

        expr = re.sub(r'([a-zA-Z0-9]+)\*\*([0-9]+)', replacer, expr)

        expr = expr.replace("*", r"\cdot ")

        return expr

    def latex_to_pixmap(self, latex_str, fontsize=14):
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, f"${latex_str}$", fontsize=fontsize)
        plt.axis('off')
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150, transparent=True)
        plt.close(fig)
        buffer.seek(0)
        image = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaledToHeight(30, Qt.TransformationMode.SmoothTransformation)
        return pixmap

    def add_item(self, fonction: str):
        if not fonction or fonction == "":
            return
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.__fonctions.append(fonction)
        self.endInsertRows()
        self.dataChangedSignal.emit()

    def remove_item(self, index: int):
        if 0 <= index < len(self.__fonctions):
            self.beginRemoveRows(QModelIndex(), index, index)
            del self.__fonctions[index]
            self.endRemoveRows()
            self.dataChangedSignal.emit()

    def get_all(self) :
        return self.__fonctions.copy()

    def to_dict(self) :
        return {"fonctions": self.__fonctions}

    @classmethod
    def from_dict(cls, data):
        if "fonctions" not in data:
            return cls([])
        return cls(data["fonctions"])

    def save_to_json(self, nom_fichier: str):
        with open(nom_fichier, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f)


    @classmethod
    def load_from_json(cls, filepath: str):
        if not os.path.exists(filepath):
            return cls([])

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return cls.from_dict(data)
        except Exception:
            return cls([])
