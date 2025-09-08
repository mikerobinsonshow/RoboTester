"""Simple demo for colored error messages."""

import logging


class _RedErrorFormatter(logging.Formatter):
    """Formatter that renders error-level logs in red."""

    _RED = "\x1b[31m"
    _RESET = "\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - trivial
        message = super().format(record)
        if record.levelno >= logging.ERROR:
            return f"{self._RED}{message}{self._RESET}"
        return message


_logger = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_handler.setFormatter(_RedErrorFormatter("%(levelname)s: %(message)s"))
_logger.addHandler(_handler)
_logger.setLevel(logging.DEBUG)


def print_hi(name: str) -> None:
    """Print a friendly greeting."""
    _logger.info(f"Hi, {name}")


if __name__ == "__main__":
    print_hi("PyCharm")
    try:
        raise ValueError("This is an error example")
    except Exception as err:  # pragma: no cover - demonstrative
        _logger.error(err)
