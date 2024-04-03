import logging
import queue
from enum import IntEnum
from multiprocessing import Process, Queue
from typing import Union

from ultralytics import YOLO
from ultralytics.utils import LOGGER as YOLO_LOGGER

from src.utils.loghandlers import QueueHandler


class YoloResults(IntEnum):
    NO_RESULTS = 0


class TrainRunner:
    """This class is responsible for training yolo models

    It is important to note that this class uses Process and two separate Queues

    log_queue: is used for logging messages to the main thread because training process runs separately
    result_queue: is used for storing the results of the training process
    """
    def __init__(self):
        self.model: Union[YOLO, None] = None
        self.log_queue = Queue()
        self.result_queue = Queue()
        self.process: Union[Process, None] = None

    def setup(self, params: dict) -> None:
        self.model = YOLO(params['model'])
        self.process = Process(target=self._train, args=(params, self.log_queue), daemon=True)

    def _train(self, params, log_queue):
        handler = QueueHandler(log_queue)
        YOLO_LOGGER.addHandler(handler)
        results = self.model.train(data=params['data'],
                                   imgsz=params['imgsz'],
                                   patience=params['patience'],
                                   epochs=params['epochs'],
                                   batch=params['batch'],
                                   save_period=params['save_period'],
                                   device=params['device'],
                                   workers=params['workers'],
                                   optimizer=params['optimizer'],
                                   verbose=True)
        if results:
            self.result_queue.put(str(results.save_dir))

    def train(self):
        if self.process:
            self.process.start()

    def stop_process(self):
        self.process.terminate()
        self.process.join()
        self.result_queue.put(None)

    def get_result(self):
        try:
            return self.result_queue.get(block=False)
        except queue.Empty:
            return YoloResults.NO_RESULTS


def val(params: dict):
    model = YOLO(params['model'])
    return model.val(data=params['data'],
                     imgsz=params['imgsz'],
                     batch=params['batch'],
                     conf=params['conf'],
                     iou=params['iou'],
                     max_det=params['max_det'],
                     device=params['device'],
                     split='test')


def predict(params: dict):
    model = YOLO(params['model'])
    return model.predict(source=params['source'],
                         conf=params['conf'],
                         iou=params['iou'],
                         device=params['device'],
                         max_det=params['max_det'],
                         save=True)
