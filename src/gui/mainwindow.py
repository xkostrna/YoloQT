import logging
from enum import IntEnum
from pathlib import Path
from typing import Union

from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QMainWindow, QSpinBox, QComboBox, QFileDialog, QGraphicsScene, QGraphicsPixmapItem,
                               QDoubleSpinBox)
from ultralytics.utils import LOGGER as YOLO_LOGGER

from src.gui.generated.ui_mainwindow import Ui_MainWindow
from src.utils import yoloiface
from src.utils.loghandlers import YoloLogHandler, MyLogHandler
from src.utils.syntaxhighlighter import SyntaxHighlighter
from src.utils.validator import is_dataset_ok, is_model_ok, YoloMode

logging.basicConfig(level=logging.INFO)


class Direction(IntEnum):
    PREV = 0
    NEXT = 1


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


class AppMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonSelectModel.clicked.connect(self.select_model)
        self.ui.pushButtonSelectDataset.clicked.connect(self.select_dataset)
        self.ui.pushButtonTrain.clicked.connect(self.train)
        self.ui.pushButtonVal.clicked.connect(self.val)
        self.ui.pushButtonLoadResults.clicked.connect(self.select_results)

        self.ui.toolButtonNext.clicked.connect(lambda _: self.change_image(Direction.NEXT))
        self.ui.toolButtonPrev.clicked.connect(lambda _: self.change_image(Direction.PREV))

        self.yolo_log_handler = YoloLogHandler(self.ui.plainTextEditLog)
        YOLO_LOGGER.addHandler(self.yolo_log_handler)

        my_log_handler = MyLogHandler(self.ui.plainTextEditLog)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt="%H:%M:%S")
        my_log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(my_log_handler)

        self.ui.splitter.splitterMoved.connect(self.splitter_moved)

        _ = SyntaxHighlighter(self.ui.plainTextEditLog.document())

        # FOR TESTING
        self.ui.lineEditSelectModel.setText(r"F:/School/Ing/DIPLOMA/YoloQT/models/yolov8n.pt")
        self.ui.lineEditSelectDataset.setText(r"F:/School/Ing/DIPLOMA/YoloQT/datasets/exdark_little/data.yaml")

        self.save_dir: Path = Path()
        self.results: list[Path] = []

    def select_model(self):
        dlg = ModelSelectDialog(self)
        dlg.fileSelected.connect(self.update_model_text)
        dlg.show()

    def update_model_text(self, text: str):
        self.ui.lineEditSelectModel.setText(text)

    def select_dataset(self):
        dlg = DatasetSelectDialog(self)
        dlg.fileSelected.connect(self.update_dataset_text)
        dlg.show()

    def update_dataset_text(self, text: str):
        self.ui.lineEditSelectDataset.setText(text)

    def select_results(self):
        dlg = LoadResultsDialog(self)
        dlg.fileSelected.connect(self.load_results)
        dlg.show()

    def load_results(self, text: str):
        self.results = [res_file for res_file in Path(text).iterdir() if res_file.suffix in [".jpg", ".png", ".jpeg"]]
        if len(self.results) == 0:
            msg = "No results or images found!"
            logging.error(msg)
            return
        self.load_image(self.results[0])

    def get_base_params(self) -> Union[dict, None]:
        model_pth = self.ui.lineEditSelectModel.text()
        dataset_pth = self.ui.lineEditSelectDataset.text()
        if model_pth == "" or dataset_pth == "":
            msg = "Please select a model and dataset first!"
            logging.error(msg)
            return None
        return {'model': Path(model_pth), 'data': Path(dataset_pth)}

    def train(self):
        params = self.get_base_params()
        if not is_model_ok(params['model'], YoloMode.TRAIN) or not is_dataset_ok(params['data'], YoloMode.TRAIN):
            return

        params.update(qobjects2dict(self.ui.groupBoxTrainArgs.children()))
        self.yolo_log_handler.reset_epochs()
        self.yolo_log_handler.total_epoch = params['epochs']
        results = yoloiface.train(params)
        if not results:
            msg = "Training failed!"
            logging.error(msg)
            return

        self.results = [res_file.absolute() for res_file in results.save_dir.iterdir()
                        if res_file.suffix in [".jpg", ".png", ".jpeg"]]
        self.load_image(self.results[0])

    def val(self):
        params = self.get_base_params()
        if not is_model_ok(params['model'], YoloMode.VAL) or not is_dataset_ok(params['data'], YoloMode.VAL):
            return

        params.update(qobjects2dict(self.ui.groupBoxValArgs.children()))
        results = yoloiface.val(params)
        if not results:
            msg = "Validation failed"
            logging.error(msg)
            return

        self.results = [res_file for res_file in results.save_dir.iterdir()
                        if res_file.suffix in [".jpg", ".png", ".jpeg"]]
        self.load_image(self.results[0])

    def load_image(self, image_path: Path):
        self.ui.lineEditCurrentImg.setText(str(image_path))

        pixmap = QPixmap(str(image_path))
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

    def change_image(self, direction: Direction):
        if len(self.results) == 0:
            msg = "First select directory with results or run training!"
            logging.error(msg)
            return
        current_img = self.ui.lineEditCurrentImg.text()
        current_idx = self.results.index(Path(current_img))
        new_idx = current_idx - 1
        if direction == Direction.NEXT:
            new_idx = current_idx + 1
        if new_idx >= len(self.results) or new_idx < 0:
            return
        self.load_image(self.results[new_idx])

    def resizeEvent(self, event):
        self.ui.graphicsView.fitInView(self.ui.graphicsView.sceneRect(), Qt.KeepAspectRatio)

    def splitter_moved(self):
        self.ui.graphicsView.fitInView(self.ui.graphicsView.sceneRect(), Qt.KeepAspectRatio)


def qobjects2dict(data: list[QObject]) -> dict:
    q_objects = [obj for obj in data if isinstance(obj, (QSpinBox, QDoubleSpinBox, QComboBox))]
    result = {}
    for obj in q_objects:
        val = obj.currentText() if isinstance(obj, QComboBox) else obj.value()
        if isinstance(val, str) and val.isdigit():
            val = int(val)
        result[obj.toolTip()] = val
    return result
