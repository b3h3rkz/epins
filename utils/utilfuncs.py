import requests
from random import randint


def send_sms(phone_number, sms_code):
    url = 'http://cheapglobalsms.com/api_v1'
    params = {
        'sub_account': '2132_bitcoin',
        'sub_account_pass': 'diamond',
        'action': 'send_sms',
        'route': 1,
        'sender_id': 'Diamond',
        'recipients': phone_number,
        'message': sms_code
    }
    send_sms = requests.post(url, params=params)
    print(send_sms.text)
    return send_sms.text


def verify_bank_account(account_number, bankcode):
    url = 'https://gwot5erqucxr9jlrx-mock.stoplight-proxy.io/api/acctinq/wrapper'
    params = {
        'bankcode': bankcode,
        'accountnumber': account_number,
        'api_key': 'HKJbdbkdskbLHlvLvcsljljjhjhvjvJjJJHjbljvjv'
    }

    send_request = requests.get(url, params)
    print(send_request.text)
    return send_request.text



