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
        if not index.isValid() or not (0 <= index.row() < len(self.__fonctions)):
            return None

        fonction = self.__fonctions[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return str(fonction)
        elif role == Qt.ItemDataRole.UserRole:
            return fonction
        elif role == Qt.ItemDataRole.ToolTipRole:
            return f"Fonction : {fonction}"
        return None

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
        with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return cls.from_dict(data)
