import logging
import re
from enum import IntEnum
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QMainWindow, QSpinBox, QComboBox, QFileDialog, QPlainTextEdit, QApplication,
                               QGraphicsScene, QGraphicsPixmapItem)
from ultralytics.utils import LOGGER as YOLO_LOGGER

from src.gui.generated.ui_mainwindow import Ui_MainWindow
from src.utils import yoloiface


class Direction(IntEnum):
    PREV = 0
    NEXT = 1


def remove_ansi_codes(s: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', s)


class MyLogHandler(logging.Handler):

    def __init__(self, plain_text_edit: QPlainTextEdit):
        super().__init__()
        self.widget = plain_text_edit

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class YoloLogHandler(logging.Handler):

    def __init__(self, plain_text_edit: QPlainTextEdit):
        super().__init__()
        self.widget = plain_text_edit
        self.total_epoch = 0
        self.current_epoch = 1

    def emit(self, record):
        msg = re.sub(r'\s+', ' ', self.format(record).strip())
        if 'Epoch' in msg:
            msg = f"Epoch {self.current_epoch}/{self.total_epoch}"
            self.current_epoch += 1
            self.widget.appendPlainText(msg)
        elif 'Model summary' in msg:
            self.widget.appendPlainText(f"\n{msg}")
        elif 'Results saved to' in msg:
            msg = remove_ansi_codes(msg)
            _, part2 = msg.split("Results saved to ")
            self.widget.appendPlainText(f"\nYou can find results here: {Path(part2).absolute()}")
        elif 'Speed:' in msg:
            self.widget.appendPlainText(msg)
        else:
            try:
                pattern = r'^(\w+)\s(-?\d+(\.\d+)?)\s(-?\d+(\.\d+)?)\s(-?\d+(\.\d+)?)\s(-?\d+(\.\d+)?)\s(-?\d+(\.\d+)?)\s(-?\d+(\.\d+)?)$'  # noqa
                if re.match(pattern, msg):
                    attribs = ['class', 'images', 'instances', 'precision', 'recall', 'map50', 'map50-95']
                    data = {name: value for name, value in zip(attribs, msg.split(' '))}
                    msg = str(data)
                    self.widget.appendPlainText(msg)
            except:
                pass
        QApplication.processEvents()


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
        self.ui.pushButtonLoadResults.clicked.connect(self.select_results)

        self.ui.toolButtonNext.clicked.connect(lambda _: self.change_image(Direction.NEXT))
        self.ui.toolButtonPrev.clicked.connect(lambda _: self.change_image(Direction.PREV))

        self.yolo_log_handler = YoloLogHandler(self.ui.plainTextEditLog)
        YOLO_LOGGER.addHandler(self.yolo_log_handler)

        my_log_handler = MyLogHandler(self.ui.plainTextEditLog)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt="%H:%M:%S")
        my_log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(my_log_handler)

        # FOR TESTING
        self.ui.lineEditSelectModel.setText(r"F:/School/Ing/DIPLOMA/YoloQT/src/models/yolov8n.pt")
        self.ui.lineEditSelectDataset.setText(r"F:/School/Ing/DIPLOMA/YoloQT/src/datasets/exdark/data.yaml")

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

    def train(self):
        model_pth = self.ui.lineEditSelectModel.text()
        dataset_pth = self.ui.lineEditSelectDataset.text()
        if model_pth == "" or dataset_pth == "":
            msg = "Please select a model and dataset first!"
            logging.error(msg)
            return

        params = {'model': Path(model_pth), 'data': Path(dataset_pth)}
        child_objects = [obj for obj in self.ui.groupBoxArguments.children() if isinstance(obj, (QSpinBox, QComboBox))]
        for child_obj in child_objects:
            val = child_obj.value() if isinstance(child_obj, QSpinBox) else child_obj.currentText()
            if isinstance(val, str) and val.isdigit():
                val = int(val)
            params[child_obj.toolTip()] = val

        self.yolo_log_handler.total_epoch = params['epochs']
        results = yoloiface.train(params)

        if not results:
            msg = "Training failed!"
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
