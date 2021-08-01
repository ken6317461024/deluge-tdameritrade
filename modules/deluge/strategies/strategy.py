"""
Base class for strategies


"""

# consistent logging
import logging
log_level = "DEBUG"
FORMAT = "%(asctime)s %(levelname)s | %(filename)s:%(lineno)s %(funcName)s | %(message)s"
logging.basicConfig(format=FORMAT, level=logging.getLevelName(log_level))
log = logging.getLogger(__name__)

class Strategy():
    def __init__(self) -> None:
        log.debug("Strategies INIT")
        pass