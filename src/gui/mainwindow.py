import logging
from enum import IntEnum
from pathlib import Path
from typing import Union

from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QMainWindow, QSpinBox, QComboBox, QGraphicsScene, QGraphicsPixmapItem,
                               QDoubleSpinBox)
from ultralytics.utils import LOGGER as YOLO_LOGGER

from src.gui.dialogs import ModelSelectDialog, DatasetSelectDialog, LoadResultsDialog, SelectImageDialog
from src.gui.generated.ui_mainwindow import Ui_MainWindow
from src.utils import yoloiface
from src.utils.device import detect_available_devices
from src.utils.loghandlers import YoloLogHandler, MyLogHandler
from src.utils.syntaxhighlighter import SyntaxHighlighter
from src.utils.validator import is_dataset_ok, is_model_ok, YoloMode, is_image_source_ok

logging.basicConfig(level=logging.INFO)


class Direction(IntEnum):
    PREV = 0
    NEXT = 1


class AppMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        _ = SyntaxHighlighter(self.ui.plainTextEditLog.document())
        self.yolo_log_handler = YoloLogHandler(self.ui.plainTextEditLog)
        YOLO_LOGGER.addHandler(self.yolo_log_handler)
        my_log_handler = MyLogHandler(self.ui.plainTextEditLog)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt="%H:%M:%S")
        my_log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(my_log_handler)
        self.init_device_combobox()

        self.ui.pushButtonSelectModel.clicked.connect(self.select_model)
        self.ui.pushButtonSelectDataset.clicked.connect(self.select_dataset)
        self.ui.pushButtonSelectSource.clicked.connect(self.select_image)
        self.ui.pushButtonTrain.clicked.connect(self.train)
        self.ui.pushButtonVal.clicked.connect(self.val)
        self.ui.pushButtonPredict.clicked.connect(self.predict)
        self.ui.pushButtonLoadResults.clicked.connect(self.select_results)

        self.ui.toolButtonNext.clicked.connect(lambda _: self.change_image(Direction.NEXT))
        self.ui.toolButtonPrev.clicked.connect(lambda _: self.change_image(Direction.PREV))

        self.ui.splitter.splitterMoved.connect(self.splitter_moved)

        # FOR TESTING
        self.ui.lineEditSelectModel.setText(r"F:/School/Ing/DIPLOMA/YoloQT/models/yolov8n.pt")
        self.ui.lineEditSelectDataset.setText(r"F:/School/Ing/DIPLOMA/YoloQT/datasets/exdark_little/data.yaml")

        self.save_dir: Path = Path()
        self.results: list[Path] = []

    def init_device_combobox(self):
        """Add items to combo box for device based available devices."""
        available_devices = detect_available_devices()
        for dev in available_devices:
            self.ui.comboBoxDevice.addItem(str(dev))
            self.ui.comboBoxDevice_2.addItem(str(dev))
            self.ui.comboBoxDevice_3.addItem(str(dev))

    def select_model(self):
        dlg = ModelSelectDialog(self)
        dlg.fileSelected.connect(lambda text: self.ui.lineEditSelectModel.setText(text))
        dlg.show()

    def select_dataset(self):
        dlg = DatasetSelectDialog(self)
        dlg.fileSelected.connect(lambda text: self.ui.lineEditSelectDataset.setText(text))
        dlg.show()

    def select_image(self):
        dlg = SelectImageDialog(self)
        dlg.fileSelected.connect(lambda text: self.ui.lineEditSource.setText(text))
        dlg.show()

    def select_results(self):
        dlg = LoadResultsDialog(self)
        dlg.fileSelected.connect(self.load_results)
        dlg.show()

    def load_results(self, text: str):
        self.results = [res_file.absolute() for res_file in Path(text).iterdir()
                        if res_file.suffix in [".jpg", ".png", ".jpeg"]]
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
        self.load_results(results.save_dir)

    def val(self):
        params = self.get_base_params()
        if not is_model_ok(params['model'], YoloMode.VAL) or not is_dataset_ok(params['data'], YoloMode.VAL):
            return
        params.update(qobjects2dict(self.ui.groupBoxValArgs.children()))
        results = yoloiface.val(params)
        if not results:
            msg = "Validation failed!"
            logging.error(msg)
            return
        self.load_results(results.save_dir)

    def predict(self):
        params = {'model': self.get_base_params().get('model')}
        if not is_model_ok(params['model'], YoloMode.VAL):
            return
        params['source'] = self.ui.lineEditSource.text()
        if not is_image_source_ok(Path(params['source'])):
            return
        params.update(qobjects2dict(self.ui.groupBoxPredictArgs.children()))
        results = yoloiface.predict(params)
        if not results:
            msg = "Prediction failed!"
            logging.error(msg)
            return
        self.load_results(results[0].save_dir)

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
    """Creates a dictionary from data which is list of QObjects.

    We only extract value or text from QSpinBox, QDoubleSpinBox a QComboBox.
    Keys in dictionary are actually toolTips of those QWidgets.
    """
    q_objects = [obj for obj in data if isinstance(obj, (QSpinBox, QDoubleSpinBox, QComboBox))]
    result = {}
    for obj in q_objects:
        val = obj.currentText() if isinstance(obj, QComboBox) else obj.value()
        if isinstance(val, str) and val.isdigit():
            val = int(val)
        result[obj.toolTip()] = val
    return result
