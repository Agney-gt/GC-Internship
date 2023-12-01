import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.FileHandler("google_search.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)
