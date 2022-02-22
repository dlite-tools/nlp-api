"""Logging Configuration module."""
from logging import (
    getLogger,
    Logger,
    StreamHandler
)
from os import getenv

from pythonjsonlogger import jsonlogger

from src.version import SERVICE_VERSION

# Environment variables
LOG_LEVEL = getenv("SERVICE_LOG_LEVEL", "INFO")
ENV = getenv("SERVICE_ENVIRONMENT", "dev")


def get_logger(name: str) -> Logger:
    """Get logger instance.

    Parameters
    ----------
    name : str
        Unique name for the logger instance

    Returns
    -------
    Logger
        Logger instance with JSON output
    """
    # Supported logging fields full list
    # https://docs.python.org/3.8/library/logging.html#logrecord-attributes

    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(module)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S.%s%z",
        rename_fields={
            "asctime": "timestamp",
            "levelname": "level"
        },
        static_fields={
            "version": SERVICE_VERSION,
            "team": "DLite",
            "environment": ENV
        }
    )

    handler = StreamHandler()
    handler.formatter = formatter

    log = getLogger(name)
    log.addHandler(handler)
    log.setLevel(LOG_LEVEL)

    return log
