'''
https://tdameritrade.readthedocs.io/en/latest/index.html#authentication
https://tdameritrade.readthedocs.io/en/latest/index.html#docs


'''
import os
import sys
import simplejson as json
import logging


log = logging.getLogger()
log.setLevel(logging.DEBUG)

# hide connection debug messages
logging.getLogger("urllib3").setLevel(logging.WARNING)



PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'modules'))


from tdameritrade_deluge import TDAmeritradeDeluge
# from deluge.allocator import Allocator
from deluge.strategies.strategyCore import StrategyCore
from deluge.strategies.strategySimple import StrategySimple


td = TDAmeritradeDeluge()
td.connect()

# accounts = td.getAccounts()
# print(json.dumps(accounts, indent=2))
# primary_account = list(accounts.keys())[0]

print(f"PRIMARY ACCOUNT ID: {td.getPrimaryAccountId()}")



# print(td.getTransactions())





sc = StrategySimple(tdAmeritrade=td)
allocation = sc.allocate(100)
print(json.dumps(allocation, indent=2))

sc.transact(allocation)





# # is market open?
# # (‘EQUITY’, ‘OPTION’, ‘FUTURE’, ‘BOND’, ‘FOREX’)
# hours = c.hours(market='EQUITY')

# # movers $COMPX, $DJI, $SPX.X
# # Dow Jones Industrial Average (DJIA or INDU)
# # S&P 500 Index (SPX)
# # Nasdaq Composite Index (COMPX)
# movers = c.movers('$COMPX')

