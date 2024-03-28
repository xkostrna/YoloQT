from PySide6.QtWidgets import QMainWindow, QFileDialog


class ModelSelectDialog(QFileDialog):
    LABEL_TEXT = "Select YOLOv8 model"
    NAME_FILTER = "PT files (*.pt);;YAML files (*.yaml)"

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setLabelText(QFileDialog.DialogLabel.LookIn, self.LABEL_TEXT)
        self.setNameFilter(self.NAME_FILTER)


class DatasetSelectDialog(QFileDialog):
    LABEL_TEXT = "Select YOLOv8 dataset"
    NAME_FILTER = "YAML files (*.yaml)"

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setLabelText(QFileDialog.DialogLabel.LookIn, self.LABEL_TEXT)
        self.setNameFilter(self.NAME_FILTER)


class LoadResultsDialog(QFileDialog):
    LABEL_TEXT = "Select directory with results"

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.setFileMode(QFileDialog.FileMode.Directory)


class SelectImageDialog(QFileDialog):
    LABEL_TEXT = "Select image"
    NAME_FILTER = "Image files (*.jpg *.jpeg *.png)"

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setLabelText(QFileDialog.DialogLabel.LookIn, self.LABEL_TEXT)
        self.setNameFilter(self.NAME_FILTER)
