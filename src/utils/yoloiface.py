import logging
from multiprocessing import Process, Queue
from typing import Union
import platform

from ultralytics import YOLO
from ultralytics.utils import LOGGER as YOLO_LOGGER

from src.utils.loghandlers import QueueHandler

# For windows DAEMON = True is working fine, however only CPU was available on development machine
DAEMON = True

# We have to fix for Unix cause threading is different there, big thanks to Ing. Pavol Marak PHDr.
# also this link was used: https://stackoverflow.com/questions/48822463/how-to-use-pytorch-multiprocessing
if platform.system() == 'Linux':
    try:
        from torch.multiprocessing import set_start_method
        set_start_method('spawn')
        DAEMON = False
    except RuntimeError as e:
        emsg = f"Torch multiprocessing spawn failed!"
        logging.error(emsg)


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
        """Prepare internal attributes for training

        :param params: dictionary of parameters for training e.g {'imgsz': 460, 'batch_size': 16 ....}
        """
        self.model = YOLO(params['model'])
        self.process = Process(target=self._train, args=(params, self.log_queue), daemon=DAEMON)

    def _train(self, params, log_queue):
        """
        This method will run after process starts, it will set handler for YOLO_LOGGER to display logs in
        main thread and then just run training.

        :param params: dictionary of parameters for training e.g {'imgsz': 460, 'batch_size': 16 ....}
        :param log_queue: Queue object where are logs put
        :return:
        """
        handler = QueueHandler(log_queue)
        YOLO_LOGGER.addHandler(handler)
        self.model.train(data=params['data'],
                         imgsz=params['imgsz'],
                         patience=params['patience'],
                         epochs=params['epochs'],
                         batch=params['batch'],
                         save_period=params['save_period'],
                         device=params['device'],
                         workers=params['workers'],
                         optimizer=params['optimizer'],
                         verbose=True)

    def train(self):
        """Starts process if it's initialized"""
        if self.process:
            self.process.start()

    def stop_process(self):
        """Forcefully tries to terminate and join process, then ends result queue."""
        self.process.terminate()
        self.process.join()
        self.result_queue.put(None)


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
