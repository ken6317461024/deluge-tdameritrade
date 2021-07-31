"""
DELUGE interface for TD Ameritrade
"""

import os
import json
import tdameritrade as _td


# consistent logging
import logging
log_level = "DEBUG"
FORMAT = "%(asctime)s %(levelname)s | %(filename)s:%(lineno)s %(funcName)s | %(message)s"
logging.basicConfig(format=FORMAT, level=logging.getLevelName(log_level))
log = logging.getLogger(__name__)


class TDAmeritradeDeluge:
    def __init__(self):
        self._td = _td

        try:
            self._client_id = os.getenv('TDAMERITRADE_CONSUMER_KEY')
        except Exception as e:
            log.warn(e)
        try:
            self._account_id = os.getenv('TDAMERITRADE_ACCOUNT')
        except Exception as e:
            log.warn(e)
        
        try:
            self._refresh_token = os.getenv('TDAMERITRADE_REFRESH_TOKEN')
        except Exception as e:
            log.warn(e)

        
        return None;

    def __str__(self):
        return("-- HELLO FROM "+__name__+" --")

    
    def connect(self):
        log.debug("TDAmeritradeDeluge CONNECT")
        self._c = self._td.TDClient(client_id=self._client_id, refresh_token=self._refresh_token, account_ids=[self._account_id])
        log.debug(f"TDAmeritradeDeluge CONNECTed? {self._c}")


    def getTransactions(self, summary=True):
        transactions = self._c.transactionsDF(type='ALL')
        summary_array = []
        for t in transactions.iloc[0,0]:
            # print(json.dumps(transactions.iloc[0,0]))
            f = t['fees']
            total_fees = f.get("rFee")+f.get("additionalFee")+f.get("cdscFee")+f.get("regFee")+f.get("otherCharges")+f.get("commission")+f.get("optRegFee")+f.get("secFee")
            summary_array.append({
                "type": f"{t['type']}: {t['description']}",
                "transactionDate": t['transactionDate'],
                "amount": t['transactionItem'].get('amount'),
                "fees": total_fees,
                "symbol": t['transactionItem'].get('instrument',{}).get('symbol')
            })
            # print(json.dumps(t, indent=2))
            # print("-"*10)

        print("\n*****")
        print(json.dumps(summary_array, indent=2))


    def getQuote(self, symbol:str):
        """
        can be single symbol or multiple
        'aapl,tsla'

        {
        "AAPL": {
            "assetType": "EQUITY",
            "assetMainType": "EQUITY",
            "cusip": "037833100",
            "symbol": "AAPL",
            "description": "Apple Inc. - Common Stock",
            "bidPrice": 145.95,
            "bidSize": 7200,
            "bidId": "P",
            "askPrice": 145.97,
            "askSize": 200,
            "askId": "P",
            "lastPrice": 145.95,
            "lastSize": 200,
            "lastId": "D",
            "openPrice": 144.38,
            "highPrice": 146.33,
            "lowPrice": 144.11,
            "bidTick": " ",
            "closePrice": 145.86,
            "netChange": 0.09,
            "totalVolume": 70440626,
            "quoteTimeInLong": 1627689582190,
            "tradeTimeInLong": 1627689598877,
            "mark": 145.86,
            "exchange": "q",
            "exchangeName": "NASD",
            "marginable": true,
            "shortable": true,
            "volatility": 0.0133,
            "digits": 4,
            "52WkHigh": 150.0,
            "52WkLow": 93.7675,
            "nAV": 0.0,
            "peRatio": 28.5226,
            "divAmount": 0.88,
            "divYield": 0.6,
            "divDate": "2021-08-06 00:00:00.000",
            "securityStatus": "Normal",
            "regularMarketLastPrice": 145.86,
            "regularMarketLastSize": 60174,
            "regularMarketNetChange": 0.0,
            "regularMarketTradeTimeInLong": 1627675200795,
            "netPercentChangeInDouble": 0.0617,
            "markChangeInDouble": 0.0,
            "markPercentChangeInDouble": 0.0,
            "regularMarketPercentChangeInDouble": 0.0,
            "delayed": false,
            "realtimeEntitled": true
        }
        }
        """
        return self._c.quote(symbol)

    
