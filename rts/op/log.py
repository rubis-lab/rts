import logging
import os


def new_logger(name='main'):
    logger = logging.getLogger(str(name))
    if not logger.handlers:
        levels = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warn': logging.WARNING,
            'warning': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG
        }
        _level = os.environ.get('RTS_LOG_LEVEL', 'info').lower()
        logger.setLevel(levels[_level])
        formatter = logging.Formatter(
            '%(asctime)s :: %(module)s :: %(funcName)s :: %(message)s')
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logger.addHandler(stream)
    return logger
