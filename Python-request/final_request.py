import hashlib
import hmac
import time
import requests
import keyboard
import uuid
import sys

API_KEY = 'yourapikey'
API_SECRET = 'yourapisecret'

def get_current_price():
    url = 'https://www.bitstamp.net/api/v2/ticker/btceur/'
    response = requests.get(url)
    data = response.json()
    bitcoin_price = data['last']
    return bitcoin_price

def api_request():
    api_url = 'yourwebhookurl'
    response = requests.get(api_url)
    if response.status_code == 200:
        content_length = response.headers.get("Content-Length")

        if content_length != "0":
            data = response.json()
            buy_price = data['price']
            return buy_price
    else:
        print(f"Error {response.status_code}: {response.text}")

def cancel_all_buy_orders(API_KEY, API_SECRET):
    timestamp = str(int(round(time.time() * 1000)))
    nonce = str(uuid.uuid4())
    content_type = 'application/x-www-form-urlencoded'

    payload = {
        'id': '0',
    }

    if sys.version_info.major >= 3:
        from urllib.parse import urlencode
    else:
        from urllib import urlencode

    payload_string = urlencode(payload)

    message = 'BITSTAMP ' + API_KEY + \
        'POST' + \
        'www.bitstamp.net' + \
        '/api/v2/cancel_all_orders/' + \
        '' + \
        content_type + \
        nonce + \
        timestamp + \
        'v2' + \
        payload_string
    message = message.encode('utf-8')
    signature = hmac.new(API_SECRET.encode(), msg=message, digestmod=hashlib.sha256).hexdigest()

    headers = {
        'X-Auth': 'BITSTAMP ' + API_KEY,
        'X-Auth-Signature': signature,
        'X-Auth-Nonce': nonce,
        'X-Auth-Timestamp': timestamp,
        'X-Auth-Version': 'v2',
        'Content-Type': content_type
    }

    r = requests.post(
        'https://www.bitstamp.net/api/v2/cancel_all_orders/',
        headers=headers,
        data=payload_string
    )

    if not r.status_code == 200:
        raise Exception('Status code not 200')

    string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')).encode('utf-8') + r.content
    signature_check = hmac.new(API_SECRET.encode(), msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()
    if not r.headers.get('X-Server-Auth-Signature') == signature_check:
        raise Exception('Signatures do not match')

    print(r.content)


def place_buy_order(API_KEY, API_SECRET, amount, current_price):
    timestamp = str(int(round(time.time() * 1000)))
    nonce = str(uuid.uuid4())
    content_type = 'application/x-www-form-urlencoded'

    payload = {
        'amount': amount,
        'price': current_price,
        'side': 'buy',
        'type': 'limit',
        'currency_pair': 'BTC/EUR'
    }

    if sys.version_info.major >= 3:
        from urllib.parse import urlencode
    else:
        from urllib import urlencode

    payload_string = urlencode(payload)

    message = 'BITSTAMP ' + API_KEY + \
        'POST' + \
        'www.bitstamp.net' + \
        '/api/v2/buy/btceur/' + \
        '' + \
        content_type + \
        nonce + \
        timestamp + \
        'v2' + \
        payload_string
    message = message.encode('utf-8')
    signature = hmac.new(API_SECRET.encode(), msg=message, digestmod=hashlib.sha256).hexdigest()
    headers = {
        'X-Auth': 'BITSTAMP ' + API_KEY,
        'X-Auth-Signature': signature,
        'X-Auth-Nonce': nonce,
        'X-Auth-Timestamp': timestamp,
        'X-Auth-Version': 'v2',
        'Content-Type': content_type
    }
    r = requests.post(
        'https://www.bitstamp.net/api/v2/buy/btceur/',
        headers=headers,
        data=payload_string
    )

    if not r.status_code == 200:
        raise Exception('Status code not 200')

    string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')).encode('utf-8') + r.content
    signature_check = hmac.new(API_SECRET.encode(), msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()
    if not r.headers.get('X-Server-Auth-Signature') == signature_check:
        raise Exception('Signatures do not match')

    print(r.content)

def place_sell_order(API_KEY, API_SECRET, amount, current_price):
    timestamp = str(int(round(time.time() * 1000)))
    nonce = str(uuid.uuid4())
    content_type = 'application/x-www-form-urlencoded'

    payload = {
        'amount': amount,
        'price': current_price,
        'side': 'sell',
        'type': 'limit',
        'currency_pair': 'BTC/EUR'
    }

    if sys.version_info.major >= 3:
        from urllib.parse import urlencode
    else:
        from urllib import urlencode

    payload_string = urlencode(payload)

    message = 'BITSTAMP ' + API_KEY + \
        'POST' + \
        'www.bitstamp.net' + \
        '/api/v2/sell/btceur/' + \
        '' + \
        content_type + \
        nonce + \
        timestamp + \
        'v2' + \
        payload_string
    message = message.encode('utf-8')
    signature = hmac.new(API_SECRET.encode(), msg=message, digestmod=hashlib.sha256).hexdigest()
    headers = {
        'X-Auth': 'BITSTAMP ' + API_KEY,
        'X-Auth-Signature': signature,
        'X-Auth-Nonce': nonce,
        'X-Auth-Timestamp': timestamp,
        'X-Auth-Version': 'v2',
        'Content-Type': content_type
    }
    r = requests.post(
        'https://www.bitstamp.net/api/v2/sell/btceur/',
        headers=headers,
        data=payload_string
    )

    if not r.status_code == 200:
        raise Exception('Status code not 200')

    string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')).encode('utf-8') + r.content
    signature_check = hmac.new(API_SECRET.encode(), msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()
    if not r.headers.get('X-Server-Auth-Signature') == signature_check:
        raise Exception('Signatures do not match')

    print(r.content)

amount = '0.0000'  # variabel ~10€ = 0.0005
#amountint = 0.0005
sell_condition = False
bitcoin_holdings = 0
saved_buy_price = 1
profit_sell = 0.0015 #variabel
loss_sell = -0.0008 #variabel

json_data = {
    'saved_buy_price': saved_buy_price
}

while True:
    buy_price = api_request()
    current_price = get_current_price()
    if bitcoin_holdings == 0 and buy_price != saved_buy_price:
        cancel_all_buy_orders(API_KEY, API_SECRET)
        place_buy_order(API_KEY, API_SECRET, amount, current_price)
        bitcoin_holdings += float(amount)
        sell_condition = True
        saved_buy_price = buy_price
        print(f"Bought {amount} Bitcoins for {current_price}!")
    
    elif sell_condition == True:
        profit_loss = (float(current_price) - float(json_data['saved_buy_price'])) / float(json_data['saved_buy_price'])
        if profit_loss >= profit_sell or profit_loss <= loss_sell:
            place_sell_order(API_KEY, API_SECRET, amount, current_price)
            bitcoin_holdings -= float(amount)
            if bitcoin_holdings == 0:
                sell_condition = False
            print(f"Sold {amount} Bitcoins for {current_price}!")
    #else:
        #print(f"No buy orders active!")

    if keyboard.is_pressed('q'):
        print("stopped API request")
        break