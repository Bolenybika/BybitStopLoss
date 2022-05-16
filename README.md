# BybitStopLoss
!!!Use at own risk, I take no responsibility for your losses!!! 
This bot is created from CryptoGnome's Bybit-Futures-Bot. It check position from coins.json every 60s and set stoploss at desired % of coins.json. 
Setup:
install Python
pip install requirements
edit settings.json with your api key & secret
edit coins.json to your desired stoploss % 
run stop_loss.py
Ps:
The calculations of the bot is not always ok especially for little price coins.
Please keep it in mind stop loss percent * your leverage, for exampe stop loss percent:3 * leverage:7 = 21
