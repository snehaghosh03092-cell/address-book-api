# logging_config.py
"""
Logging configuration for Address Book API.
Provides a named logger with INFO level and structured format.
"""
import logging

# -------------------------------
# Basic logger configuration
# -------------------------------
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT
)

# Named logger for your application
logger = logging.getLogger("address_book_api")