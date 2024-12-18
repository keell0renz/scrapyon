import logging

logger = logging.getLogger("scrapyon")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


def setup_logging(verbose: bool):
    """Configure logging based on verbose setting"""
    logger.setLevel(logging.INFO if verbose else logging.WARNING)
    # Remove any existing handlers to avoid duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    # Add our handler
    logger.addHandler(handler)  # type: ignore
