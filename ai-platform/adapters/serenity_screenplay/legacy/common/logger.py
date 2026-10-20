import logging


def get_logger(name: str) -> logging.Logger:
    """Return a consistently configured application logger."""
    logger = logging.getLogger(name)
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )
    return logger
