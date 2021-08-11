"""
CORE portfolio strategy
https://docs.google.com/spreadsheets/d/1WCTA5vStYPJYZQkbMKvKtd38gCSW_KPQipbmKDEDYkA/edit#gid=1464948463


Well-diversified portfolio


"""

import os
import sys
import json
import math
import tdameritrade as _td

# consistent logging
import logging
log_level = "DEBUG"
FORMAT = "%(asctime)s %(levelname)s | %(filename)s:%(lineno)s %(funcName)s | %(message)s"
logging.basicConfig(format=FORMAT, level=logging.getLevelName(log_level))
log = logging.getLogger(__name__)


from deluge.strategies.strategy import Strategy


class StrategySimple(Strategy):
    
    
    def __init__(self, tdAmeritrade=None) -> None:
        super().__init__(tdAmeritrade)
        log.debug(f"StrategyCore INIT {self._td}")


    def allocate(self,total=0):
        """
        set up our allocation
        """
        symbols = [
            {"s": "GPRO", "p":.5, "a": "buy"},
            # {"s": "XRX", "p":.05, "a": "buy"}

        ]
        allocation = self._allocator.calculate(symbols, total)
        return allocation
        
