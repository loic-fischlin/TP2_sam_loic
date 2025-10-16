import json
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal

class ListeFonctionsModel(QAbstractListModel):
    dataChangedSignal = pyqtSignal()

    def __init__(self, fonctions=None):
        super().__init__()
        self._fonctions = fonctions or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._fonctions)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._fonctions)):
            return None

        fonction = self._fonctions[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return str(fonction)
        elif role == Qt.ItemDataRole.UserRole:
            return fonction
        elif role == Qt.ItemDataRole.ToolTipRole:
            return f"Fonction : {fonction}"
        return None

    def add_item(self, fonction: str):
        if not fonction or fonction.strip() == "":
            return
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._fonctions.append(fonction.strip())
        self.endInsertRows()
        self.dataChangedSignal.emit()

    def remove_item(self, index: int):
        if 0 <= index < len(self._fonctions):
            self.beginRemoveRows(QModelIndex(), index, index)
            del self._fonctions[index]
            self.endRemoveRows()
            self.dataChangedSignal.emit()

    def update_item(self, index: int, nouvelle_fonction: str):
        if 0 <= index < len(self._fonctions) and nouvelle_fonction:
            self._fonctions[index] = nouvelle_fonction.strip()
            top_left = self.index(index, 0)
            bottom_right = self.index(index, 0)
            self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole])
            self.dataChangedSignal.emit()

    def get_all(self) -> list[str]:
        return self._fonctions.copy()

    def to_dict(self) -> dict:
        return {"fonctions": self._fonctions}

    @classmethod
    def from_dict(cls, data: dict):
        if not isinstance(data, dict) or "fonctions" not in data:
            return cls([])
        return cls(fonctions=data["fonctions"])

    def save_to_json(self, nom_fichier: str):
        with open(nom_fichier, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f)


    @classmethod
    def load_from_json(cls, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return cls.from_dict(data)
