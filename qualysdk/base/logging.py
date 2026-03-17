"""
Logging helpers for qualysdk.

qualysdk is a library, so it installs a NullHandler by default and leaves
handler selection to the caller. CLI entrypoints can opt into the packaged
formatter with configure_logging().
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from threading import Lock, Thread
from time import monotonic, sleep
from typing import IO, Callable, Iterable

LOG_FORMAT = (
    "%(asctime)s - %(levelname)s - %(name)s - "
    "%(funcName)s - L%(lineno)d - %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_QUALYSDK_HANDLER_NAME = "qualysdk_stream_handler"


package_logger = logging.getLogger("qualysdk")
package_logger.addHandler(logging.NullHandler())


@dataclass
class ProgressTracker:
    """
    Emit periodic progress summaries without spamming a log line per page.
    """

    logger: logging.Logger
    operation: str
    item_label: str
    item_interval: int | None = None
    page_interval: int | None = None
    chunk_interval: int | None = None
    time_interval: float = 20.0
    total_pages: int | None = None
    total_chunks: int | None = None
    remaining_label: str = "chunk(s) remaining"
    level: int = logging.INFO
    _items: int = field(default=0, init=False, repr=False)
    _pages: int = field(default=0, init=False, repr=False)
    _chunks: int = field(default=0, init=False, repr=False)
    _started_at: float = field(default_factory=monotonic, init=False, repr=False)
    _last_report_at: float = field(default_factory=monotonic, init=False, repr=False)
    _last_report_items: int = field(default=0, init=False, repr=False)
    _last_report_pages: int = field(default=0, init=False, repr=False)
    _last_report_chunks: int = field(default=0, init=False, repr=False)
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def record(
        self,
        *,
        items: int = 0,
        pages: int = 0,
        chunks: int = 0,
        queue_remaining: int | None = None,
        extra: str | None = None,
        force: bool = False,
    ) -> None:
        with self._lock:
            self._items += items
            self._pages += pages
            self._chunks += chunks
            now = monotonic()
            if not self._should_emit(now, force=force):
                return
            self._emit("progress", now, queue_remaining=queue_remaining, extra=extra)

    def complete(self, *, queue_remaining: int | None = None, extra: str | None = None) -> None:
        with self._lock:
            self._emit("complete", monotonic(), queue_remaining=queue_remaining, extra=extra)

    def _should_emit(self, now: float, *, force: bool) -> bool:
        if force:
            return True

        progress_made = any(
            [
                self._items != self._last_report_items,
                self._pages != self._last_report_pages,
                self._chunks != self._last_report_chunks,
            ]
        )
        if not progress_made:
            return False

        if self.item_interval and (self._items - self._last_report_items) >= self.item_interval:
            return True
        if self.page_interval and (self._pages - self._last_report_pages) >= self.page_interval:
            return True
        if self.chunk_interval and (self._chunks - self._last_report_chunks) >= self.chunk_interval:
            return True

        return bool(self.time_interval and (now - self._last_report_at) >= self.time_interval)

    def _emit(
        self,
        status: str,
        now: float,
        *,
        queue_remaining: int | None = None,
        extra: str | None = None,
    ) -> None:
        elapsed = int(now - self._started_at)
        message_parts = [f"{self.operation} {status}: {self._items:,} {self.item_label}"]

        if self._pages:
            if self.total_pages is not None:
                message_parts.append(f"{self._pages:,}/{self.total_pages:,} page(s) complete")
            else:
                message_parts.append(f"{self._pages:,} page(s) complete")

        if self._chunks:
            if self.total_chunks is not None:
                message_parts.append(f"{self._chunks:,}/{self.total_chunks:,} chunk(s) complete")
            else:
                message_parts.append(f"{self._chunks:,} chunk(s) complete")

        if queue_remaining is not None:
            message_parts.append(f"{queue_remaining:,} {self.remaining_label}")

        message_parts.append(f"{elapsed}s elapsed")

        if extra:
            message_parts.append(extra)

        self.logger.log(self.level, ", ".join(message_parts))
        self._last_report_at = now
        self._last_report_items = self._items
        self._last_report_pages = self._pages
        self._last_report_chunks = self._chunks


def wait_for_threads_with_heartbeat(
    threads: Iterable[Thread],
    *,
    progress: ProgressTracker | None = None,
    heartbeat_interval: float = 120.0,
    poll_interval: float = 1.0,
    heartbeat_extra: str = "still running",
    queue_remaining_getter: Callable[[], int | None] | None = None,
) -> None:
    """
    Wait for a thread group to finish while emitting periodic heartbeat logs.
    """

    thread_list = list(threads)
    last_heartbeat = monotonic()

    while any(thread.is_alive() for thread in thread_list):
        now = monotonic()
        if (
            progress is not None
            and heartbeat_interval
            and (now - last_heartbeat) >= heartbeat_interval
        ):
            progress.record(
                queue_remaining=queue_remaining_getter() if queue_remaining_getter else None,
                extra=heartbeat_extra,
                force=True,
            )
            last_heartbeat = now
        sleep(poll_interval)

    for thread in thread_list:
        thread.join()


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
