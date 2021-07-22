import os
from loguru import logger
from loguru._logger import Logger


class Logger():
    def __init__(self, level: str, filename: str) -> None:
        """
        - Args:
            - level: int, log level
            - filename: str, log file name
        """
        filename = os.path.join(
            os.path.dirname(__file__),
            "../..",
            filename
        )

        logger.add(filename, rotation="0:00", level=level,
                   filter=lambda record: record["extra"].get("name") == filename)
        self._logger = logger.bind(name=filename)

    def logger(self) -> Logger:
        return self._logger
