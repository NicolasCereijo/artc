import logging
import colorlog


def setup_logger():
    """
        Configure the logger with a colored formatter and set the logging level to INFO.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s - %(message)s',
        log_colors={
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
