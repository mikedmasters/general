import websocket
import json

import talib
import numpy

from binance.client import Client
from binance.enums import *

API_KEY = ' '# Your Personal API Key given to you from Binance
API_SECRET = ' ' # Your Secret API Key given to you from Binance

client = Client(API_KEY, API_SECRET)

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 13
RSI_OVERSOLD = 32
TRADE_SYMBOL = "ETHUSDT"
TRADE_QUANTITY = .02

closes =[]
in_position = False
n = 0
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print ("Sending Order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity = quantity)
        print (order)

    except Exception as e:
        return False
    return True

def on_open(ws):
    print ('Opened Connection')

def on_close(ws):
    print('Connection Closed')

def on_message(ws, message):
    global n 
    global in_position
    global closes
    # print('recieved message')    
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    if is_candle_closed:
        print("candle closed at {}".format(close))        
        closes.append(float(close))

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            # print("all rsis calculated so far")
            # print (rsi)
            last_rsi = rsi[-1]
            print("The current rsi is{}".format(last_rsi))

            if last_rsi < RSI_OVERSOLD:
                print ("Purchases made:",n)
                print ("OVERSOLD!")
                if in_position:
                    print('It is oversold, but you already own it. Checking to see if you have maxed ordered...')
                    if n >=2:
                        print('Maxe Order Reached - 2 orderes complete')
                else:
                    if ((n == 1) and (last_rsi < 20)):
                        print ("Buying second round")
                        order1 = client.create_order(symbol='ETHUSDT', side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity = .02)
                        print (order1)
                        if order1:
                            print ("SECOND ORDER COMPLETE")
                            order = client.get_my_trades(symbol=TRADE_SYMBOL, limit=1)
                            order = (order[0])
                            pur_price =  (order['price'])
                            target = pur_price*1.0025
                            print("TARGET PRICE FOR SALE: ", target)
                            order1 = client.create_order(symbol='ETHUSDT', side=Client.SIDE_SELL, type=Client.ORDER_TYPE_LIMIT, quantity = .02, price = target )
                            n=n+1
                            in_position = True
                    if n ==0:
                        print ("buy, buy, buy")
                        order1 = client.create_order(symbol='ETHUSDT', side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity = .02)
                        print (order1)
                        if order1:
                            print ("ORDER COMPLETE")
                            order = client.get_my_trades(symbol=TRADE_SYMBOL, limit=1)
                            order = (order[0])
                            pur_price =  (order['price'])
                            target = pur_price*1.0025
                            print("TARGET PRICE FOR SALE: ", target)
                            order1 = client.create_order(symbol='ETHUSDT', side=Client.SIDE_SELL, type=Client.ORDER_TYPE_LIMIT, quantity = .02, price = target)
                            n=n+1
                            in_position = True

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()
