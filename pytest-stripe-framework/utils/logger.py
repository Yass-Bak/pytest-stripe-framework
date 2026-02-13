import logging
import sys
from .config import Config

class Logger:
    _logger = None

    @classmethod
    def get_logger(cls):
        if cls._logger:
            return cls._logger
        
        logger = logging.getLogger("StripeTestFramework")
        logger.setLevel(Config.LOG_LEVEL)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s'
        ))
        
        logger.addHandler(console_handler)
        cls._logger = logger
        return logger

logger = Logger.get_logger()
