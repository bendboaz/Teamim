import logging
import sys
from pathlib import Path
import warnings
from datetime import datetime

START_TIME = datetime.now().strftime('%e-%m-%y_%H-%M-%S').lstrip()


def get_log_filename(name):
    return f'{name}-{START_TIME}.log'


def init_logger(name, dir_path=None, to_screen=True):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('{asctime} - {message}', datefmt="%H:%M:%S", style="{")
    handlers = []
    if to_screen:
        handlers.append(logging.StreamHandler(sys.stdout))
    if dir_path is not None:
        path = Path(dir_path) / get_log_filename(name)
        Path(dir_path).mkdir(exist_ok=True, parents=True)
        handlers.append(logging.FileHandler(path))

    if len(handlers) == 0:
        warnings.warn(f'No handlers for logger {name}, output will not be saved')

    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
