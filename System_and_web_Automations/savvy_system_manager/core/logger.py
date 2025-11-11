# core/logger.py
import logging
import os

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "system_log.txt")

logger = logging.getLogger("savvy_system")
logger.setLevel(logging.INFO)

# avoid adding multiple handlers if reloaded
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)


def log_action(message, level="info"):
    """Write message to file logger. level: 'info'|'error'|'warning'."""
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    else:
        logger.info(message)
