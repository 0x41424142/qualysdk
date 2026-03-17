from json import dump
from qualysdk.base.logging import get_logger

logger = get_logger(__name__)


def write_json(data: dict, output: str) -> None:
    with open(output, "w") as f:
        dump(data, f, indent=2)
    logger.info(f"Data written to {output}.")
