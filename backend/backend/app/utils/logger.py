import logging
import sys

# Configure logger
logger = logging.getLogger("masterdsa")
logger.setLevel(logging.DEBUG)

# Console handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)

logger.addHandler(handler)