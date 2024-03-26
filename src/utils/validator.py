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


def is_imgset_valid(imgset: Union[str, None]) -> bool:
    if not imgset:
        return False
    if not Path(imgset).is_dir():
        return False
    return (Path(imgset).parent / "labels").is_dir()


def get_dataset_state(dataset_pth: Path, mode: YoloMode) -> DatasetState:
    if not dataset_pth.exists():
        return DatasetState.NOT_EXIST
    if dataset_pth.suffix != '.yaml':
        return DatasetState.WRONG_SUFFIX

    data = yaml.safe_load(dataset_pth.read_text())

    if mode == YoloMode.TRAIN:
        for img_set in ['train', 'val']:

            img_set_pth = data.get(img_set)

            if not img_set_pth:
                return DatasetState.WRONG_FORMAT

            if not Path(img_set_pth).exists():
                return DatasetState.WRONG_FORMAT

            if not img_set_pth:
                return DatasetState.WRONG_FORMAT

            possible_pth = (dataset_pth / data[img_set]).resolve()

            if not possible_pth.exists():
                return DatasetState.WRONG_FORMAT

        return DatasetState.OK

    possible_pth = (dataset_pth / data['test']).resolve()

    print((dataset_pth / data['train']).resolve())
    print((dataset_pth / data['val']).resolve())
    print((dataset_pth / data['test']).resolve())
    print(data)
    return DatasetState.OK
