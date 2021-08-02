"""
Base class for strategies


"""

# consistent logging
import logging
log_level = "DEBUG"
FORMAT = "%(asctime)s %(levelname)s | %(filename)s:%(lineno)s %(funcName)s | %(message)s"
logging.basicConfig(format=FORMAT, level=logging.getLevelName(log_level))
log = logging.getLogger(__name__)



from deluge.allocator import Allocator


class Strategy():
    def __init__(self, tdAmeritrade=None) -> None:
        log.debug("Strategies INIT")
        self._td = tdAmeritrade;
        self._allocator = Allocator(tdAmeritrade=self._td)
        pass