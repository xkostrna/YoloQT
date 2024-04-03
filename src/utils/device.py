import logging

import torch


# https://stackoverflow.com/questions/48152674/how-do-i-check-if-pytorch-is-using-the-gpu
def detect_available_devices():
    """Returns a list of available devices

    Example of output:
        if cuda detected: [0, 'cpu']
        otherwise:        ['cpu']
    """
    available_devices = []
    try:
        cuda_dev_id = torch.cuda.current_device()
        if cuda_dev_id >= 0:
            available_devices.append(cuda_dev_id)
        msg = "CUDA device detected!"
        logging.info(msg)
    except AssertionError:
        msg = "No CUDA devices detected => 'cpu' will be set as default device."
        logging.warning(msg)
    available_devices.append('cpu')
    return available_devices
