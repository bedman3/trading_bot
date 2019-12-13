import logging
import os
import sys

from main.util.time import get_utc_plus_8_time_now

datetime_to_date_strftime_pattern = '%Y_%m_%d'
project_base_path = os.path.dirname(__file__)


def get_logger(name: str, file_name: str = 'martin_trading_bot') -> logging.Logger:
    log_folder = os.path.join(project_base_path, 'logs')
    if not os.path.isdir(log_folder):
        os.makedirs(log_folder)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # create file handler which logs even debug messages
    today_date = get_utc_plus_8_time_now(datetime_format=True).strftime(
        datetime_to_date_strftime_pattern)
    file_name = f'{file_name}-{today_date}.log'
    file_dir = os.path.join(log_folder, file_name)
    fh = logging.FileHandler(file_dir, mode='a')
    fh.setLevel(logging.INFO)

    # create console handler with a higher log level
    stdout_sh = logging.StreamHandler(sys.stdout)
    stdout_sh.setLevel(logging.INFO)
    stderr_sh = logging.StreamHandler(sys.stderr)
    stderr_sh.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    stdout_sh.setFormatter(formatter)
    stderr_sh.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(stdout_sh)
    logger.addHandler(stderr_sh)

    return logger
