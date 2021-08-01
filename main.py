'''
https://tdameritrade.readthedocs.io/en/latest/index.html#authentication
https://tdameritrade.readthedocs.io/en/latest/index.html#docs


'''
import os
import sys
import json
import logging


log = logging.getLogger()
log.setLevel(logging.DEBUG)

# hide connection debug messages
logging.getLogger("urllib3").setLevel(logging.WARNING)



PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'modules'))


from tdameritrade_deluge import TDAmeritradeDeluge
from deluge.allocator import Allocator


td = TDAmeritradeDeluge()
td.connect()
# print(td.getTransactions())

# q =td.getQuote('aapl,tsla')
# print(json.dumps(q, indent=2))

# a = Allocator(tdAmeritrade=td)
# print(a)

# symbols = [
#     {"s": "aapl", "p":.5},
#     {"s": "tsla", "p": .4},
#     {"s": "vigi", "p": .1}
# ]
# allocation = a.calculate(symbols, 1000.45)
# print(json.dumps(allocation, indent=2))


from deluge.strategies.strategyCore import StrategyCore

sc = StrategyCore()



# import os
# import tdameritrade as td

# client_id = os.getenv('TDAMERITRADE_CONSUMER_KEY')
# account_id = os.getenv('TDAMERITRADE_ACCOUNT')
# refresh_token = os.getenv('TDAMERITRADE_REFRESH_TOKEN')

# c = td.TDClient(client_id=client_id, refresh_token=refresh_token, account_ids=[account_id])


# # see all transactions in account
# print(c.transactions(type='ALL'))
# # or
# transactions = c.transactionsDF(type='ALL')
# transactions.iloc[0,0]


# # Fundamentals for a company
# aapl = c.fundamentalSearchDF('AAPL')
# print(aapl['fundamental'][0])


# # is market open?
# # (‘EQUITY’, ‘OPTION’, ‘FUTURE’, ‘BOND’, ‘FOREX’)
# hours = c.hours(market='EQUITY')

# # movers $COMPX, $DJI, $SPX.X
# # Dow Jones Industrial Average (DJIA or INDU)
# # S&P 500 Index (SPX)
# # Nasdaq Composite Index (COMPX)
# movers = c.movers('$COMPX')

