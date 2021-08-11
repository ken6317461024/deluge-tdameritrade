"""
DELUGE interface for TD Ameritrade
"""

import os
import json
import tdameritrade as _td


# consistent logging
import logging

log_level = "DEBUG"
FORMAT = (
    "%(asctime)s %(levelname)s | %(filename)s:%(lineno)s %(funcName)s | %(message)s"
)
logging.basicConfig(format=FORMAT, level=logging.getLevelName(log_level))
log = logging.getLogger(__name__)


class TDAmeritradeDeluge:
    def __init__(self):
        self._td = _td

        try:
            self._client_id = os.getenv("TDAMERITRADE_CONSUMER_KEY")
        except Exception as e:
            log.warn(e)
        try:
            self._account_id = os.getenv("TDAMERITRADE_ACCOUNT")
        except Exception as e:
            log.warn(e)

        try:
            self._refresh_token = os.getenv("TDAMERITRADE_REFRESH_TOKEN")
        except Exception as e:
            log.warn(e)

        return None

    def __str__(self):
        return "-- HELLO FROM " + __name__ + " --"

    def connect(self):
        log.debug("TDAmeritradeDeluge CONNECT")
        self._c = self._td.TDClient(
            client_id=self._client_id,
            refresh_token=self._refresh_token,
            account_ids=[self._account_id],
        )
        log.debug(f"TDAmeritradeDeluge CONNECTed? {self._c}")

    """
    
    https://developer.tdameritrade.com/account-access/apis/get/accounts-0
    """

    def getAccounts(self):
        return self._c.accounts()

    def getPrimaryAccountId(self):
        accounts = self.getAccounts()

        # we assume the first account is primary
        return list(accounts.keys())[0]

    def getTransactions(self, summary=True):
        transactions = self._c.transactionsDF(type="ALL")
        summary_array = []
        for t in transactions.iloc[0, 0]:
            # print(json.dumps(transactions.iloc[0,0]))
            f = t["fees"]
            total_fees = (
                f.get("rFee")
                + f.get("additionalFee")
                + f.get("cdscFee")
                + f.get("regFee")
                + f.get("otherCharges")
                + f.get("commission")
                + f.get("optRegFee")
                + f.get("secFee")
            )
            summary_array.append(
                {
                    "type": f"{t['type']}: {t['description']}",
                    "transactionDate": t["transactionDate"],
                    "amount": t["transactionItem"].get("amount"),
                    "fees": total_fees,
                    "symbol": t["transactionItem"].get("instrument", {}).get("symbol"),
                }
            )
            # print(json.dumps(t, indent=2))
            # print("-"*10)

        print("\n*****")
        print(json.dumps(summary_array, indent=2))

    def getQuote(self, symbol: str):
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

    """
    PLACE AN ORDER
    
    https://developer.tdameritrade.com/content/place-order-samples
    https://developer.tdameritrade.com/account-access/apis/post/accounts/%7BaccountId%7D/orders-0
    
    
    {
    "session": "'NORMAL' or 'AM' or 'PM' or 'SEAMLESS'",
    "duration": "'DAY' or 'GOOD_TILL_CANCEL' or 'FILL_OR_KILL'",
    "orderType": "'MARKET' or 'LIMIT' or 'STOP' or 'STOP_LIMIT' or 'TRAILING_STOP' or 'MARKET_ON_CLOSE' or 'EXERCISE' or 'TRAILING_STOP_LIMIT' or 'NET_DEBIT' or 'NET_CREDIT' or 'NET_ZERO'",
    "cancelTime": {
        "date": "string",
        "shortFormat": false
    },
    "complexOrderStrategyType": "'NONE' or 'COVERED' or 'VERTICAL' or 'BACK_RATIO' or 'CALENDAR' or 'DIAGONAL' or 'STRADDLE' or 'STRANGLE' or 'COLLAR_SYNTHETIC' or 'BUTTERFLY' or 'CONDOR' or 'IRON_CONDOR' or 'VERTICAL_ROLL' or 'COLLAR_WITH_STOCK' or 'DOUBLE_DIAGONAL' or 'UNBALANCED_BUTTERFLY' or 'UNBALANCED_CONDOR' or 'UNBALANCED_IRON_CONDOR' or 'UNBALANCED_VERTICAL_ROLL' or 'CUSTOM'",
    "quantity": 0,
    "filledQuantity": 0,
    "remainingQuantity": 0,
    "requestedDestination": "'INET' or 'ECN_ARCA' or 'CBOE' or 'AMEX' or 'PHLX' or 'ISE' or 'BOX' or 'NYSE' or 'NASDAQ' or 'BATS' or 'C2' or 'AUTO'",
    "destinationLinkName": "string",
    "releaseTime": "string",
    "stopPrice": 0,
    "stopPriceLinkBasis": "'MANUAL' or 'BASE' or 'TRIGGER' or 'LAST' or 'BID' or 'ASK' or 'ASK_BID' or 'MARK' or 'AVERAGE'",
    "stopPriceLinkType": "'VALUE' or 'PERCENT' or 'TICK'",
    "stopPriceOffset": 0,
    "stopType": "'STANDARD' or 'BID' or 'ASK' or 'LAST' or 'MARK'",
    "priceLinkBasis": "'MANUAL' or 'BASE' or 'TRIGGER' or 'LAST' or 'BID' or 'ASK' or 'ASK_BID' or 'MARK' or 'AVERAGE'",
    "priceLinkType": "'VALUE' or 'PERCENT' or 'TICK'",
    "price": 0,
    "taxLotMethod": "'FIFO' or 'LIFO' or 'HIGH_COST' or 'LOW_COST' or 'AVERAGE_COST' or 'SPECIFIC_LOT'",
    "orderLegCollection": [
        {
            "orderLegType": "'EQUITY' or 'OPTION' or 'INDEX' or 'MUTUAL_FUND' or 'CASH_EQUIVALENT' or 'FIXED_INCOME' or 'CURRENCY'",
            "legId": 0,
            "instrument": "The type <Instrument> has the following subclasses [Equity, FixedIncome, MutualFund, CashEquivalent, Option] descriptions are listed below\"",
            "instruction": "'BUY' or 'SELL' or 'BUY_TO_COVER' or 'SELL_SHORT' or 'BUY_TO_OPEN' or 'BUY_TO_CLOSE' or 'SELL_TO_OPEN' or 'SELL_TO_CLOSE' or 'EXCHANGE'",
            "positionEffect": "'OPENING' or 'CLOSING' or 'AUTOMATIC'",
            "quantity": 0,
            "quantityType": "'ALL_SHARES' or 'DOLLARS' or 'SHARES'"
        }
    ],
    "activationPrice": 0,
    "specialInstruction": "'ALL_OR_NONE' or 'DO_NOT_REDUCE' or 'ALL_OR_NONE_DO_NOT_REDUCE'",
    "orderStrategyType": "'SINGLE' or 'OCO' or 'TRIGGER'",
    "orderId": 0,
    "cancelable": false,
    "editable": false,
    "status": "'AWAITING_PARENT_ORDER' or 'AWAITING_CONDITION' or 'AWAITING_MANUAL_REVIEW' or 'ACCEPTED' or 'AWAITING_UR_OUT' or 'PENDING_ACTIVATION' or 'QUEUED' or 'WORKING' or 'REJECTED' or 'PENDING_CANCEL' or 'CANCELED' or 'PENDING_REPLACE' or 'REPLACED' or 'FILLED' or 'EXPIRED'",
    "enteredTime": "string",
    "closeTime": "string",
    "accountId": 0,
    "orderActivityCollection": [
        "\"The type <OrderActivity> has the following subclasses [Execution] descriptions are listed below\""
    ],
    "replacingOrderCollection": [
        {}
    ],
    "childOrderStrategies": [
        {}
    ],
    "statusDescription": "string"
}

//The class <Instrument> has the 
//following subclasses: 
//-Equity
//-FixedIncome
//-MutualFund
//-CashEquivalent
//-Option
//JSON for each are listed below: 

//Equity:
{
  "assetType": "'EQUITY' or 'OPTION' or 'INDEX' or 'MUTUAL_FUND' or 'CASH_EQUIVALENT' or 'FIXED_INCOME' or 'CURRENCY'",
  "cusip": "string",
  "symbol": "string",
  "description": "string"
}

//OR

//FixedIncome:
{
  "assetType": "'EQUITY' or 'OPTION' or 'INDEX' or 'MUTUAL_FUND' or 'CASH_EQUIVALENT' or 'FIXED_INCOME' or 'CURRENCY'",
  "cusip": "string",
  "symbol": "string",
  "description": "string",
  "maturityDate": "string",
  "variableRate": 0,
  "factor": 0
}

//OR

//MutualFund:
{
  "assetType": "'EQUITY' or 'OPTION' or 'INDEX' or 'MUTUAL_FUND' or 'CASH_EQUIVALENT' or 'FIXED_INCOME' or 'CURRENCY'",
  "cusip": "string",
  "symbol": "string",
  "description": "string",
  "type": "'NOT_APPLICABLE' or 'OPEN_END_NON_TAXABLE' or 'OPEN_END_TAXABLE' or 'NO_LOAD_NON_TAXABLE' or 'NO_LOAD_TAXABLE'"
}

//OR

//CashEquivalent:
{
  "assetType": "'EQUITY' or 'OPTION' or 'INDEX' or 'MUTUAL_FUND' or 'CASH_EQUIVALENT' or 'FIXED_INCOME' or 'CURRENCY'",
  "cusip": "string",
  "symbol": "string",
  "description": "string",
  "type": "'SAVINGS' or 'MONEY_MARKET_FUND'"
}

//OR

//Option:
{
  "assetType": "'EQUITY' or 'OPTION' or 'INDEX' or 'MUTUAL_FUND' or 'CASH_EQUIVALENT' or 'FIXED_INCOME' or 'CURRENCY'",
  "cusip": "string",
  "symbol": "string",
  "description": "string",
  "type": "'VANILLA' or 'BINARY' or 'BARRIER'",
  "putCall": "'PUT' or 'CALL'",
  "underlyingSymbol": "string",
  "optionMultiplier": 0,
  "optionDeliverables": [
    {
      "symbol": "string",
      "deliverableUnits": 0,
      "currencyType": "'USD' or 'CAD' or 'EUR' or 'JPY'",
      "assetType": "'EQUITY' or 'OPTION' or 'INDEX' or 'MUTUAL_FUND' or 'CASH_EQUIVALENT' or 'FIXED_INCOME' or 'CURRENCY'"
    }
  ]
}

//The class <OrderActivity> has the 
//following subclasses: 
//-Execution
//JSON for each are listed below: 

//Execution:
{
  "activityType": "'EXECUTION' or 'ORDER_ACTION'",
  "executionType": "'FILL'",
  "quantity": 0,
  "orderRemainingQuantity": 0,
  "executionLegs": [
    {
      "legId": 0,
      "quantity": 0,
      "mismarkedQuantity": 0,
      "price": 0,
      "time": "string"
    }
  ]
}
    """

    def placeOrder(self, allocation: dict) -> dict:

        primary_account_id = self.getPrimaryAccountId()
        results = []

        for a in allocation["allocation"]:

            log.debug("ORDER: ")
            log.debug(a)
            o = a["order"]

            # order = {
            #     "orderType": "LIMIT",
            #     "session": "NORMAL",
            #     "price": f"{o['price']}",
            #     "duration": "GOOD_TILL_CANCEL",
            #     "orderStrategyType": "TRIGGER",
            #     "orderLegCollection": [
            #         {
            #             "instruction": f"{o['action'].upper()}",
            #             "quantity": f"{o['qty']}",
            #             "instrument": {"symbol": f"{o['symbol']}", "assetType": "EQUITY"},
            #         }
            #     ],
            #     "childOrderStrategies": [
            #         {
            #             "orderType": "LIMIT",
            #             "session": "NORMAL",
            #             "price": f"{o['stop_price']}",
            #             "duration": "GOOD_TILL_CANCEL",
            #             "orderStrategyType": "SINGLE",
            #             "orderLegCollection": [
            #                 {
            #                     "instruction": "SELL",
            #                     "quantity": f"{o['qty']}",
            #                     "instrument": {"symbol": f"{o['symbol']}", "assetType": "EQUITY"},
            #                 }
            #             ],
            #         }
            #     ],
            # }
            order = {
                "orderType": "LIMIT",
                "session": "NORMAL",
                "price": f"{o['price']}",
                "duration": "GOOD_TILL_CANCEL",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "Buy",
                        "quantity": o['qty'],
                        "instrument": {"symbol": f"{o['symbol']}", "assetType": "EQUITY"},
                    }
                ],
            }

            print("*" * 10)
            log.debug(json.dumps(order, indent=2))
            print("*" * 10)

            try:
                self._c.session.headers = {"Content-Type": "application/json"}
                # result = self._c.placeOrder(accountId=primary_account_id, order=order)
                # result = self._c.placeOrder(accountId=primary_account_id, json=order)
                result = self._c.placeOrder(accountId=primary_account_id, order=json.dumps(order))
                results.append(result)
                log.info("ORDER RESULT:")
                log.info(json.dumps(result, indent=2))
            except Exception as e:
                log.warn(f"UNABLE TO PLACE ORDER: {e}")

        return results
