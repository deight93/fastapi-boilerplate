import logging
from logging import getLogger
from pathlib import Path

import logfire

# Adding the logfire handler

LOG_DIR = Path(__file__).parent.parent
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE_PATH = LOG_DIR / "logs" / "app.log"

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    handlers=[logfire.LogfireLoggingHandler()],
    level=LOGGING_LEVEL,
    format=LOGGING_FORMAT,
)
#
# file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=10485760, backupCount=5)
# file_handler.setLevel(LOGGING_LEVEL)
# file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
#
# logging.getLogger("").addHandler(file_handler)


def setup_logger(name):
    logger = getLogger(name)
    # sending all logs starting from the DEBUG level
    logger.setLevel("DEBUG")
    return logger
