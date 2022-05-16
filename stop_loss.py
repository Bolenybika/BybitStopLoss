
import requests
from datetime import datetime
from time import sleep
import time
import json
import logging
from prettyprinter import pprint
import bybitwrapper

with open('settings.json', 'r') as fp:
    settings = json.load(fp)
fp.close()
with open('coins.json', 'r') as fp:
    coins = json.load(fp)
fp.close()

client = bybitwrapper.bybit(test=False, api_key=settings['key'], api_secret=settings['secret'])


def load_jsons():
    print("Checking Settings")
    with open('coins.json', 'r') as fp:
        coins = json.load(fp)
    fp.close()
    with open('settings.json', 'r') as fp:
        settings = json.load(fp)
    fp.close()

def load_symbols(coins):
    symbols = []
    for coin in coins:
        symbols.append(coin['symbol'])
    return symbols

def check_positions_long(symbol):
    positions = client.LinearPositions.LinearPositions_myPosition(symbol=symbol+"USDT").result()
    if positions[0]['ret_msg'] == 'OK':
        for position in positions[0]['result']:
            if position['position_idx'] < 2 and position['entry_price'] > 0:
                print("Position found for ", symbol, " entry price of ", position['entry_price'])
                return position
            else:
                pass

    else:
        print("API NOT RESPONSIVE AT CHECK ORDER")
        sleep(5)
 
def fetch_ticker_long(symbol):
    position = check_positions_long(symbol)
    ticker_long = float(position['entry_price'])
    return ticker_long


def fetch_stop_price_long(symbol, side):
    ticker_long = fetch_ticker_long(symbol)
    for coin in coins:
        if coin['symbol'] == symbol:
            if side == 'Buy':
                price = round(ticker_long - (ticker_long * (coin['stop_loss_percent'] / 100)), 3)
                side = 'Sell'
                return price, side, price
            else:
                side = 'Buy'
                price = round(ticker_long + (ticker_long * (coin['stop_loss_percent'] / 100)), 3)
                return price, side, ticker
        else:
            pass




def set_sl_long(symbol, size, side):
    prices = fetch_stop_price_long(symbol, side)
    orders = client.LinearConditional.LinearConditional_getOrders(symbol=symbol + "USDT", limit='5').result()
    print("Setting Stop Loss ", symbol)
    order = client.LinearPositions.LinearPositions_tradingStop(symbol=symbol+"USDT", side="Buy", stop_loss=prices[0])                                                .result()

    pprint(order)
def fetch_positions_long():

    for coin in coins:
        symbol = coin['symbol']

        position = check_positions_long(symbol)

        if position != None:
            
            
            set_sl_long(symbol, position['size'], position['side'])
        else:
            pass



def check_positions(symbol):
    positions = client.LinearPositions.LinearPositions_myPosition(symbol=symbol+"USDT").result()
    if positions[0]['ret_msg'] == 'OK':
        for position in positions[0]['result']:
            if position['position_idx'] > 1 and position['entry_price'] > 0:
                print("Position found for ", symbol, " entry price of ", position['entry_price'], position['side'])
                return position
            else:
                pass

    else:
        print("API NOT RESPONSIVE AT CHECK ORDER")
        sleep(5)
 
def fetch_ticker(symbol):
    position = check_positions(symbol)
    ticker = float(position['entry_price'])
    return ticker



def fetch_stop_price(symbol, side):
    ticker = fetch_ticker(symbol)
    for coin in coins:
        if coin['symbol'] == symbol:
            if side == 'Buy':
                price = round(ticker - (ticker * (coin['stop_loss_percent'] / 100)), 3)
                side = 'Sell'
                return price, side, price
            else:
                side = 'Buy'
                price = round(ticker + (ticker * (coin['stop_loss_percent'] / 100)), 3)
                return price, side, ticker
        else:
            pass




def set_sl(symbol, size, side):
    prices = fetch_stop_price(symbol, side)
    orders = client.LinearConditional.LinearConditional_getOrders(symbol=symbol + "USDT", limit='5').result()
    print("Setting Stop Loss ", symbol)
    order = client.LinearPositions.LinearPositions_tradingStop(symbol=symbol+"USDT", side="Sell", stop_loss=prices[0])                                          .result()

    pprint(order)
def fetch_positions():

    for coin in coins:
        symbol = coin['symbol']

        position = check_positions(symbol)

        if position != None:
            
            
            set_sl(symbol, position['size'], position['side'])
        else:
           pass


load_jsons()

print("Starting  Stoploss")
while True:
    print("Checking for Positions.........")
    fetch_positions_long()
    time.sleep(2)
    fetch_positions()
    sleep(settings['cooldown'])

