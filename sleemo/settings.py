import logging
from typing import List

from sleemo.logging import ContextLogger
from sleemo.logging import JsonFormatter


class Logging(object):
    """Logging setting class."""

    def __init__(
        self,
        logger: logging.Logger = ContextLogger('sleemo'),    # type: ignore
        handlers: List[logging.Handler] = [logging.StreamHandler()],
        log_level: int = logging.INFO,
        correlation_attr_name: str = 'correlation_id'
    ):
        """
        Create new logging setting.

        Parameters
        ----------
        logger: logging.Logger
            Logger
        handlers: List[logging.Handler]
            Logging handlers
        log_level: int = logging.INFO
            Log level
        correlation_attr_name: str = 'correlation_id'
            The attribute name of log records for correlation
        """
        f = JsonFormatter()
        for h in handlers:
            h.setFormatter(f)
            logger.addHandler(h)
        logger.setLevel(log_level)
        self.logger = logger
        self.correlation_attr_name = correlation_attr_name

