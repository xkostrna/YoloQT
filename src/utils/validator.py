import logging
from pathlib import Path
from enum import IntEnum
from typing import Union
import yaml


class DatasetState(IntEnum):
    OK = 0
    NOT_EXIST = 1
    WRONG_SUFFIX = 2
    WRONG_FORMAT = 3


class YoloMode(IntEnum):
    TRAIN = 0
    VAL = 1


def is_imgset_valid(dataset_pth: Path, imgset: Union[str, None]) -> bool:
    """Image set is valid when it exists, it's directory and has labels directory.

    examples of input: C:/datasets/exdark/train/images
                       C:/datasets/exdark/train
    """
    if not imgset:
        return False

    imgset_pth = Path(imgset)

    if not imgset_pth.is_absolute():
        imgset_pth = dataset_pth / imgset_pth

    if not imgset_pth.is_dir():
        return False

    if imgset_pth.name == 'images':
        return (imgset_pth.parent / 'labels').is_dir()
    return (imgset_pth / 'labels').is_dir()


def get_dataset_state(dataset_pth: Path, mode: YoloMode) -> DatasetState:
    """Check if .yaml file describing dataset is valid, if it contains valid information."""
    if not dataset_pth.exists():
        return DatasetState.NOT_EXIST
    if dataset_pth.suffix != '.yaml':
        return DatasetState.WRONG_SUFFIX

    data = yaml.safe_load(dataset_pth.read_text())

    if mode == YoloMode.TRAIN:
        for img_set in ['train', 'val']:
            if not is_imgset_valid(dataset_pth, data.get(img_set)):
                return DatasetState.WRONG_FORMAT
        return DatasetState.OK

    return DatasetState.OK if is_imgset_valid(dataset_pth, data.get('test')) else DatasetState.WRONG_FORMAT


def is_dataset_ok(dataset_pth: Path, yolo_mode: YoloMode) -> bool:
    """Handles various states of dataset, return's True if dataset passes checks."""
    dataset_state = get_dataset_state(dataset_pth, yolo_mode)
    if dataset_state == DatasetState.OK:
        msg = "Dataset is OK!"
        logging.info(msg)
        return True
    elif dataset_state == DatasetState.NOT_EXIST:
        msg = "Dataset does not exist!"
        logging.error(msg)
    elif dataset_state == DatasetState.WRONG_SUFFIX:
        msg = "Dataset should be describe in .yaml file!"
        logging.error(msg)
    elif dataset_state.WRONG_FORMAT:
        msg = "Dataset does not meet the required yolo format!"
        logging.error(msg)
    return False


def is_model_ok(model_pth: Path, yolo_mode: YoloMode) -> bool:
    """Checks if path provided points to existing file with corresponding type."""
    if not model_pth.is_file():
        msg = "Model file does not exist or is not a file!"
        logging.error(msg)
        return False
    elif yolo_mode == YoloMode.TRAIN and model_pth.suffix not in ['.pt', '.yaml']:
        msg = "Wrong data type of model file!"
        logging.error(msg)
        return False
    elif yolo_mode == YoloMode.VAL and model_pth.suffix != '.pt':
        msg = "Cannot use untrained model for inference!"
        logging.error(msg)
        return False
    msg = "Model file is OK!"
    logging.info(msg)
    return True
