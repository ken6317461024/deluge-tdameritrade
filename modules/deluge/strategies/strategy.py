"""
Base class for strategies


"""

import simplejson as json

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


    """
    TRANSACT AN ALLOCATION

    buy or sell the number of shares indicated by the allocation

    """
    def transact(self, allocation=None) -> None:
        log.info("-"*10)
        log.info("TRANSACT")
        self._td.placeOrder(allocation)
        log.info("-"*10)