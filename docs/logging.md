# Logging

qualysdk uses the standard Python `logging` module for internal status, progress,
warning, and error messages.

## Default behavior

As a library, qualysdk installs a `NullHandler` on the top-level `qualysdk` logger.
That means importing and using the SDK will not automatically emit log output unless
your application configures logging.

## Quick start

If you want qualysdk logs with the packaged formatter, call `configure_logging()`:

```py
from qualysdk import configure_logging

configure_logging()
```

By default this configures the `qualysdk` logger hierarchy at `INFO` level.

## Format

The packaged formatter includes:

- Timestamp
- Log level
- Logger name
- Function name
- Line number
- Message

The emitted format is:

```text
%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - L%(lineno)d - %(message)s
```

## Logger hierarchy

qualysdk uses module-level loggers such as:

- `qualysdk.base.call_api`
- `qualysdk.vmdr.get_host_list`
- `qualysdk.was.scans`

If you prefer to integrate with your own logging setup, configure the standard Python
logging system for the `qualysdk` namespace instead of calling `configure_logging()`.

## Public helpers

qualysdk exposes two helpers:

- `configure_logging(...)`: Attach a stream handler using the packaged formatter.
- `get_logger(name)`: Return a logger in the qualysdk namespace.

Example:

```py
from qualysdk import configure_logging, get_logger

configure_logging(level="DEBUG")
logger = get_logger("qualysdk.example")
logger.debug("custom message")
```

## CLI behavior

The bundled CLI entrypoints call `configure_logging()` automatically, so SDK progress
messages appear during CLI use without extra setup.

User-facing command output still writes to standard output where appropriate. Logging
messages are separate from that output.
