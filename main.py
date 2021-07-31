'''
https://tdameritrade.readthedocs.io/en/latest/index.html#authentication
https://tdameritrade.readthedocs.io/en/latest/index.html#docs


'''

import os
import tdameritrade as td

client_id = os.getenv('TDAMERITRADE_CONSUMER_KEY')
account_id = os.getenv('TDAMERITRADE_ACCOUNT')
refresh_token = os.getenv('TDAMERITRADE_REFRESH_TOKEN')

c = td.TDClient(client_id=client_id, refresh_token=refresh_token, account_ids=[account_id])

print(c.transactions(type='ALL'))