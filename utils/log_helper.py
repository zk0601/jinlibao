import logging


def logger(path, level=logging.DEBUG):
    logger = logging.getLogger(path)
    logger.setLevel(level)
    fmt = logging.Formatter('%(asctime)s %(filename)s:[line:%(lineno)d] %(levelname)s %(message)s')
    fh = logging.FileHandler(path, 'a', encoding='UTF-8')
    fh.setFormatter(fmt)
    fh.setLevel(level)
    logger.addHandler(fh)
    return logger


def request_log(path, level=logging.DEBUG):
    logger = logging.getLogger(path)
    logger.setLevel(level)
    fmt = logging.Formatter('')
    fh = logging.FileHandler(path, 'a', encoding='UTF-8')
    fh.setFormatter(fmt)
    fh.setLevel(level)
    logger.addHandler(fh)
    return logger
