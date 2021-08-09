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


class StrategyCore(Strategy):
    
    
    def __init__(self, tdAmeritrade=None) -> None:
        super().__init__(tdAmeritrade)
        log.debug(f"StrategyCore INIT {self._td}")


    def allocate(self,total=0):
        """
        set up our allocation
        """
        symbols = [
            {"s": "VIG", "p":.05, "a": "buy"},
            {"s": "SCHG", "p": .06, "a": "buy"},
            {"s": "SCHD", "p": .06, "a": "buy"},
            {"s": "SPYD", "p": .08, "a": "buy"},
            {"s": "FNDX", "p": .08, "a": "buy"},
            {"s": "FNDB", "p": .045, "a": "buy"},
            {"s": "FNDA", "p": .05, "a": "buy"},
            {"s": "ARKK", "p": .03, "a": "buy"},
            {"s": "ARKF", "p": .02, "a": "buy"},
            {"s": "ARKG", "p": .04, "a": "buy"},
            {"s": "ARKQ", "p": .04, "a": "buy"},
            {"s": "ARKX", "p": .02, "a": "buy"},
            {"s": "ESGV", "p": .05, "a": "buy"},
            {"s": "DSI", "p": .05, "a": "buy"},
            {"s": "SMLV", "p": .02, "a": "buy"},
            {"s": "XSLV", "p": .02, "a": "buy"},
            {"s": "IJR", "p": .02, "a": "buy"},
            {"s": "SCHP", "p": .04, "a": "buy"},
            {"s": "SUB", "p": .01, "a": "buy"},
            {"s": "VIGI", "p": .05, "a": "buy"},
            {"s": "FNDF", "p": .05, "a": "buy"},
            {"s": "PALL", "p": .025, "a": "buy"},
            {"s": "CPER", "p": .025, "a": "buy"},
            {"s": "JJN", "p": .025, "a": "buy"},
            {"s": "IAU", "p": .04, "a": "buy"},
        ]
        allocation = self._allocator.calculate(symbols, total)
        return allocation
        
