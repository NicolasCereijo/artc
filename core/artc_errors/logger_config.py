import logging
import colorlog


class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        """
        Configure the logger with a colored formatter and set the logging level to INFO.
        """
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

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
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
