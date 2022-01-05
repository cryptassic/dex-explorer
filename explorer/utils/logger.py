import logging
import coloredlogs

class CustomLogger:

    def __new__(cls):
        logger = logging.getLogger("CustomLogger")
        
        coloredlogs.install(
            logger=logger, fmt="%(asctime)s [%(levelname)s] - %(message)s")

        return logger