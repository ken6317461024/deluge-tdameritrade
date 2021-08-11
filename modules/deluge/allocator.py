"""
BASKET ALLOCATOR

given a list of stocks, percentages and total to invest
returns # of shares to purchase

"""
import os
import sys
import json
import math
from decimal import *
import tdameritrade as _td

# consistent logging
import logging
log_level = "DEBUG"
FORMAT = "%(asctime)s %(levelname)s | %(filename)s:%(lineno)s %(funcName)s | %(message)s"
logging.basicConfig(format=FORMAT, level=logging.getLevelName(log_level))
log = logging.getLogger(__name__)

#Decimal precision
getcontext().prec = 4


class Allocator:
    def __init__(self, tdAmeritrade=None):
        log.debug("Allocator INIT")
        self._td = tdAmeritrade;

    def __str__(self):
        return("-- HELLO FROM "+__name__+" --")


    # pass in array of ojects
    # s: symbol
    # p: percentage
    # a: action: buy or sell
    # total: total to invest in this allocation
    # lookup current price
    # calculate # of shares 
    # return [{symbol: AAPL, shares:45}]
    def calculate(self, symbols: list, total: float)-> list:
        log.debug(f"Allocator.calculate() total: {total}")
        
        symbol_string = ""
        percent_total = Decimal(0)

        # iterate to build quotes, sanity check
        for s in symbols:
            symbol_string += f"{s['s']},"
            percent_total += Decimal(s['p'])

            if percent_total > 1:
                sys.exit(f"EXIT: allocation is over 100%: {percent_total}")

        # trim trailing comma (aapl,tsla,)
        symbol_string = symbol_string[0:-1]
        log.debug(f"looking up: {symbol_string}")

        quotes = self._td.getQuote(symbol_string)
        # print(json.dumps(quotes, indent=2))

        # calculate totals for this allocation
        meta_shares_to_buy = 0
        meta_shares_to_sell = 0
        meta_dollars_to_buy = 0
        meta_dollars_to_sell = 0


        allocation = []
        for s in symbols:
            q = quotes[s['s'].upper()]
            # print(f"{q['symbol']}: last: {q['lastPrice']}  ( bid: {q['bidPrice']} ask: {q['askPrice']}, spread: {(q['askPrice'] - q['bidPrice']):.2f} )")
            dollars = Decimal(total * s['p'])
            shares_fractional = dollars / Decimal(q['lastPrice'])
            # shares = math.ceil(shares_fractional)
            shares = round(shares_fractional)
            amount_to_purchase = shares * q['lastPrice']

            if s['a'] == 'buy':
                meta_shares_to_buy += shares
                meta_dollars_to_buy += Decimal(amount_to_purchase)
            if s['a'] == 'sell':   
                meta_shares_to_sell += shares
                meta_dollars_to_sell += Decimal(amount_to_purchase)

        
            # profit and stop-loss calculations
            last_price = Decimal(q['lastPrice'])
            trailing_stop_percent = Decimal(.05)
            stop_price = last_price - (last_price * trailing_stop_percent)
            profit_target_percent = Decimal(.1)
            profit_target = last_price+ (last_price * profit_target_percent)

        
            # print(f"total: {total}, percent: {s['p']*100}% dollars: {dollars:.2f} shares: {shares}, amount: {amount_to_purchase},  shares raw: {shares_fractional:.2f} ")
            allocation.append({
                "order": {
                    "symbol": s['s'].upper(),
                    "percent": s['p'],
                    "action": s['a'],
                    "qty": shares,
                    "amount": amount_to_purchase,
                    "shares_fractional": shares_fractional,
                    "price": q['lastPrice'],
                    "dollars": dollars,
                    "stop_price": stop_price,
                    "profit_target": profit_target
                    }
            })

        allocation_obj = {}
        allocation_obj['allocation'] = allocation

        allocation_obj['meta'] = {
            "ALLOCATION_TOTALS":{
                "shares_to_buy": meta_shares_to_buy,
                "shares_to_sell": meta_shares_to_sell,
                "dollars_to_buy": float(meta_dollars_to_buy),
                "dollars_to_sell": float(meta_dollars_to_sell),
                "percentage_total": percent_total
            }
        }

        return allocation_obj
