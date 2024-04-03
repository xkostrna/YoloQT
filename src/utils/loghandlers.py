import logging
import re
import threading
from pathlib import Path

from PySide6.QtWidgets import QPlainTextEdit, QApplication


def remove_ansi_codes(s: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', s)


class LogListenerThread(threading.Thread):
    def __init__(self, log_queue, handler):
        super().__init__()
        self.log_queue = log_queue
        self.handler = handler

    def run(self):
        while True:
            record = self.log_queue.get()
            if record is None:
                break
            self.handler.emit(record)


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class MyLogHandler(logging.Handler):

    def __init__(self, plain_text_edit: QPlainTextEdit):
        super().__init__()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt="%H:%M:%S")
        self.setFormatter(formatter)
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

    def reset_epochs(self):
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
        elif 'epochs completed in' in msg:
            self.widget.appendPlainText(msg)
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
