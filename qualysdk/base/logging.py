"""
Logging helpers for qualysdk.

qualysdk is a library, so it installs a NullHandler by default and leaves
handler selection to the caller. CLI entrypoints can opt into the packaged
formatter with configure_logging().
"""

from __future__ import annotations

import logging
from typing import IO

LOG_FORMAT = (
    "%(asctime)s - %(levelname)s - %(name)s - "
    "%(funcName)s - L%(lineno)d - %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_QUALYSDK_HANDLER_NAME = "qualysdk_stream_handler"


package_logger = logging.getLogger("qualysdk")
package_logger.addHandler(logging.NullHandler())


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a logger in the qualysdk hierarchy.
    """
    return logging.getLogger(name or "qualysdk")


def configure_logging(
    level: int | str = logging.INFO,
    stream: IO[str] | None = None,
    logger_name: str = "qualysdk",
    propagate: bool = False,
) -> logging.Logger:
    """
    Configure a stream handler for the qualysdk logger hierarchy.

    Args:
        level: Logging level as an int or standard level name.
        stream: Optional output stream for the handler.
        logger_name: Logger namespace to configure. Defaults to "qualysdk".
        propagate: Whether configured logs should bubble up to parent loggers.
    """
    logger = logging.getLogger(logger_name)

    if isinstance(level, str):
        parsed_level = logging.getLevelNamesMapping().get(level.upper())
        if parsed_level is None:
            raise ValueError(f"Invalid logging level: {level}")
        level = parsed_level

    logger.setLevel(level)
    logger.propagate = propagate

    handler = next(
        (
            existing_handler
            for existing_handler in logger.handlers
            if getattr(existing_handler, "name", None) == _QUALYSDK_HANDLER_NAME
        ),
        None,
    )
    if handler is None:
        handler = logging.StreamHandler(stream=stream)
        handler.name = _QUALYSDK_HANDLER_NAME
        logger.addHandler(handler)
    elif stream is not None:
        handler.setStream(stream)

    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    return logger
