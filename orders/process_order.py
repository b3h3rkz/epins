import requests
ONE_BTC = 100000000


def validate_address(address, coin):
    url = 'https://shapeshift.io/validateAddress/' + address + '/' + coin
    res = requests.get(url)
    valid = dict(res.json())
    valid = list(valid.values())
    return valid[0]


def get_fee():
    recommended_fee = 15
    res = requests.get('https://bitcoinfees.earn.com/api/v1/fees/recommended')
    res = dict(res.json())
    if res['fastestFee'] < 60:
        recommended_fee += res['fastestFee']
        return recommended_fee
    else:
        return 50


def to_btc(amount):
    url = 'https://blockchain.info/tobtc?currency=USD&value=' + str(amount)
    res = requests.get(url)
    res = float(res.text)
    amount = ONE_BTC * res
    return amount


def send(address, amount):
    amount = to_btc(amount)
    guid = '82f06008-1438-4fbe-82f0-96537b6b866c'
    url = 'http://localhost:3000/merchant/' + guid + '/payment'
    params = {
        'password': "BOBlane9090..",
        'second_password': 'BOBlane9090...',
        'to': address,
        'amount': 1,
        'from': 0,
        'fee_per_byte': 5
    }
    send_payment = requests.get(url, params=params)
    return send_payment.json()


def account_balance():
    """
    check the account balance of the user to ensure that they have enough funds to perform the transaction
    :return: Boolean
    """
    pass




