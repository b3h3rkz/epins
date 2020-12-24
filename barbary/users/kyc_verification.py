import requests
from django.conf import settings


def verify_bank_acct(account_number, bank_code, user):
    url = "https://gwot5erqucxr9jlrx-mock.stoplight-proxy.io/api/sacctinq/bvn/wrapper"

    payload = {"bank_code": str(bank_code),
               "account_number": str(account_number),
               "api_key":"HKJbdbkdskbLHlvLvcsljljjhjhvjvJjJJHjbljvjv"
               }

    headers = {'content-type': 'application/json'}
    response = requests.request("POST", url, json=payload, headers=headers)
    response = response.json()
    print(response['responses'][0]['status'])
    if response['responses'][0]['status'] == str(200):
            account_name = response['responses'][0]['firstname'] + " " + response['responses'][0]['lastname']
            print(account_name)
            if is_similar(user, account_name):
                return True
            else:
                return False
    else:
        return False


def get_bvn_info(bvn_number):
    """
    get the information of the user from this endpoint
    BVN Validation is only available for Nigerian customers. It allows you verify BVN supplied by a customer and
    can also be used for customer KYC methods such as; validating date of birth supplied by the customer,
    validating the mobile number, first name & last name etc.

    To use the endpoint, it is split into two flows:
    1. The customer supplied the BVN.
    2. We send an OTP to the customer which they pass to you. When it's passed to you:
    3. you validate and get the response containing the BVN details returned to you.

    :param bvn_number:
    :param api_endpoint:
    :return:
    """
    data = {
        "bvn": bvn_number,
        "seckey": "FLWSECK-b86e4802fc5eaa03db5e7f73fdc4514e-X",
        "otpoption": "SMS"
    }
    response = requests.post(settings.BVN_API_ENDPOINT, data=data)
    print(response.content)
    return response.json()


"""
 All methods that are prefixed with inclusive_ are meant for verifying Ghanaian accounts using the InclusiveFT API
 Verification Methods:
 1. Passport
 2. Voters Card
 3. Driver's License
 4. SSNIT 
 GET : https://api.inclusiveft.com/v1/GH/
 
"""

headers = {
    'content-type': "application/json",
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjRmMTJjN2E2ZTczZmJhN"
                     "zBmZmM4M2VlZjIyMTEzZDNlMzcwOWZhZDEzMTIwODE5MDU3ZDgyMDU1OTk4NjM0OGMzZDg2Mm"
                     "Q1NzRjYmUyMzIzIn0.eyJhdWQiOiIxIiwianRpIjoiNGYxMmM3YTZlNzNmYmE3MGZmYzgzZWVm"
                     "MjIxMTNkM2UzNzA5ZmFkMTMxMjA4MTkwNTdkODIwNTU5OTg2MzQ4YzNkODYyZDU3NGNiZTIzMjM"
                     "iLCJpYXQiOjE1MjkzNTYxOTQsIm5iZiI6MTUyOTM1NjE5NCwiZXhwIjoxNTYwODkyMTk0LCJzdWI"
                     "iOiI2MiIsInNjb3BlcyI6W119.m2SiketHCdYY-OA983Q2nmQBA27Yz9AVDKxMjaKLBBrzuP7Jyd"
                     "3hUVPb9kZFyuLfBom4R96j1UBE6o6aMx-ZkXx9Miexj4snhSsMXk0AhTraD-1FOA7t5Xy6cQdGh"
                     "iydvPYm8_J2Q3StU2A9RjPo_xgh-ddJnozWA0FgIDNUB5HA9s8_XB6eqCLSXZbSqtFNovMXUhak1-f"
                     "dEVNM0em7ea3nPI4bhV-2DL-27Mmp-Vph46lCCGoKZ1KtSLV9M7Z7SLXREbQClxnPYdNrA3_t6Lxx-"
                     "hSbsZ5IPWDXacRHFYs5_4XgdIOVab635QSuRZYVnzyr39wzsqDUUPfxdl9ev5r3MHsDYeUV5SC-I7E"
                     "NQ2Rxbf4S6AaYIlOaVNjaa6-PyxnblJxkEM9R2LJKCPUEz0vn7Y4XrGofYjNIhZ1H44KXh--nye1yXH"
                     "zaRQxWDffxny8OefzpVXGsmuo3Mbafpus2FlKWbmEZDg_D7Rlx3MvBTxGemUxOQzz2SFrQ634k4aYty"
                     "GLdbd7-hJEP8h1JSNhDbKREOcP0wpJgAFQIksDuuU6lN18CqaBZ3Qu7PEDNr93WuuLtTcPcAuXFrkCNr2B"
                     "3h3ivCvA0PbzL1C--OyTGdGuO8Dwj3Bb-XoRx-p9o3sSA3z4jP8AWPuiVHpmRmEmM5tocig8Fz0_W1eTxdX8",
    'accept': 'application/json',
}

# url = settings.INCLUSIVE_FT_API

# response = {'status': 200, 'success': True,
# 'data': {'id': '5702038018', 'pollingStation': 'C020409B', 'name': 'KWABENA OKYIRE APPIANING',
# 'age': 32, 'gender': 'M', 'issuedOn': '2012-04-21'}}

# response = {"status":400, "error":{"code":404,"message":"Invalid Voter's id number"}}


def inclusive_account_info():
    """
    get account information of the account
    :return: `Response  string`
    """
    response = requests.request("GET", url, headers=headers)
    return response.text


def inclusive_voter_card(id_number):
    """
    verify user using voters card number
    :param id_number
    :return: `Response JSON <Object>`
    """
    response = requests.get(url + 'voter', params={'id': id_number}, headers=headers)
    if response['status'] == 200:
        name = transform_name(response['data']['name'])
    if response['status'] == 400:
        return not_found(response)
    return name


def inclusive_passport(id_number):
    """
    verify user using voters card number
    :param id_number
    :return: `Response JSON <Object>`
    """
    response = requests.get(url + 'passport', params={'id': id_number}, headers=headers)
    if response['status'] == 200:
        name = transform_name(response['data']['name'])
    if response['status'] == 400:
        return not_found(response)
    return name


def inclusive_ssnit(id_number):
    """
      verify user using SSNIT
      :param id_number
      :return: `Response JSON <Object>`
    """
    response = requests.get(url + 'voter', params={'id': id_number}, headers=headers)
    if response['status'] == 200:
        name = transform_name(response['data']['name'])
    if response['status'] == 400:
        return not_found(response)
    return name


def inclusive_driver_license(first_name, last_name):
    """
    verify user using driver's license
    :param first_name
    :param last_name
    :return: `Response JSON <Object>`
    """
    response = requests.get(url + 'voter', params={
        'first_name': first_name,
        'last_name': last_name
    }, headers=headers)

    if response['status'] == 400:
        return not_found(response)
    return response.json()


def transform_name(name):
    """
    the name of the user is returned as a list for easy comparison with the user's saved name on Bitnob
    :param name:
    :return: List of the user's name in lower string format
    """
    name = [n.lower() for n in name.split()]
    return name


def is_similar(fullname, verification_name):
        """
        compare the data (full name) of the user received by the API with the user's registered name
        :param fullname:  the name of the user on this website
        :param verification_name the name gotten from the verification endpoint
        :return: bool: True if there are 2 or more similar names
        """
        similarity = set(fullname).intersection(verification_name)
        similarity_metric = set(fullname.split()) == set(verification_name.split())
        print(fullname, verification_name)
        print(similarity_metric)
        if similarity_metric:
            return True
        else:
            return False
        # if len(similarity) > 1:
        #     print("yes")
        #     return True
        # else:
        #     print("no")
        #     return True


def not_found(response):
    """
    generice error message
    :return: Json
    """
    response = {"message": response['error']['message'],  "status": 400}
    return response

