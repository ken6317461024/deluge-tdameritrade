"""
CORE portfolio strategy

"""

# consistent logging
import logging
log_level = "DEBUG"
FORMAT = "%(asctime)s %(levelname)s | %(filename)s:%(lineno)s %(funcName)s | %(message)s"
logging.basicConfig(format=FORMAT, level=logging.getLevelName(log_level))
log = logging.getLogger(__name__)


from deluge.strategies.strategy import Strategy


class StrategyCore(Strategy):
    
    
    def __init__(self) -> None:
        super().__init__()
        log.debug("StrategyCore INIT")
