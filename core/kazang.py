import requests
import json
import django
from datetime import datetime
from django.conf import settings
from .models import KazangSession
from time import sleep
from threading import Thread

now = datetime.now().isoformat()

base_url = "https://api.kazang.net/apimanager/api_rest/v1/"
prod_username = "8011819587"
prod_password = "*HJe;PJx6g"
channel = "PridePayments"
serial_number = "102.147.160.102"
time_stamp = now
auth_data = {
    "username": prod_username, "password": prod_password, "channel": channel
}

headers = {
    "Content-Type": "application/json"

}


def auth_client():
    r = requests.post(base_url + "authClient", data=json.dumps(auth_data), headers=headers)
    return r.json()


def get_new_session_uuid():
    session_uuid = auth_client().get('session_uuid', False)
    return session_uuid


def get_active_session_uuid():
    """
    Used for getting the last saved session uuid from the database.
    """
    session = KazangSession.objects.all().last()
    return session.session_uuid

def get_or_create_session_uuid():
    db_session = KazangSession.objects.all().last().session_uuid
    data = {"session_uuid": db_session}
    products = requests.post(base_url + 'productList', data=json.dumps(data), headers=headers)
    if products.json().get('response_code', False) == 0:
        return db_session
    else:
        return get_new_session_uuid()

session_uuid = get_or_create_session_uuid()


def get_balance():
    return auth_client().get('balance', None)


def is_session_active(response):
    return response.json().get('response_code', False) == 0


data = {
    "session_uuid": session_uuid
}
default_data = {
    'session_uuid': session_uuid
}


def product_list():
    r = requests.post(base_url + 'productList', data=json.dumps(default_data), headers=headers)
    return r.json()

def find_product_from_method_name(method: str):
    """
    Get a product dictionary form an API method name
    :param method:
    :return dict:
    """
    products = product_list()
    return next(item for item in products if item["method_name"] == method)


def airtel_pay_payment(phone_number: str, amount):
    data = {
        "session_uuid": session_uuid
    }
    """
    Airtel Pay Payment workflow
    :param phone_number:
    :param amount:
    :return:
    """
    data['product_id'] = '5392'
    data['wallet_msisdn'] = phone_number
    data['amount'] = amount
    r = requests.post(base_url + "airtelPayPayment", data=json.dumps(data), headers=headers)
    confirmation_number = r.json().get('confirmation_number', False)
    data['confirmation_number'] = confirmation_number
    result = requests.post(base_url + "airtelPayPaymentConfirm", data=json.dumps(data), headers=headers)
    return result.json()


def airtel_pay_query():
    pass
    # airtel_reference = result.json().get('airtel_reference', False)
    # data['airtel_reference'] = airtel_reference
    # data['product_id'] = "5393"
    # airtel_pay_query = requests.post(base_url + "airtelPayQuery", data=json.dumps(data), headers=headers)
    # data['confirmation_number'] = airtel_pay_query.json().get('confirmation_number', False)
    # airtel_pay_query_confirm = requests.post(base_url + "airtelPayQueryConfirm", data=json.dumps(data), headers=headers)
    #
    # return airtel_pay_query_confirm.json()


def zamtelMoneyPay(phone_number: str, amount):
    data = {
        "session_uuid": session_uuid
    }
    """Zamtel Money Pay workflow"""
    data['request_reference'] = '100402'
    data['msisdn'] = phone_number
    data['amount'] = amount
    data['product_id'] = '1706'
    zamtel_money_pay = requests.post(base_url + 'zamtelMoneyPay', data=json.dumps(data), headers=headers)
    data['request_reference'] = '128001'
    data['confirmation_number'] = zamtel_money_pay.json().get('confirmation_number', None)
    zamtel_pay_confirmation = requests.post(base_url + 'zamtelMoneyPayConfirm', data=json.dumps(data), headers=headers)
    return zamtel_pay_confirmation.json()


def mtn_debit(phone_number: str, amount: float):
    data['wallet_msisdn'] = phone_number
    data['amount'] = amount
    data['product_id'] = '1612'
    r = requests.post(base_url + 'mtnDebit', data=json.dumps(data), headers=headers)
    data['supplier_transaction_id'] = r.json().get('supplier_transaction_id', None)
    data['product_id'] = '1613'
    approval = requests.post(base_url + 'mtnDebitApproval', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = approval.json().get('confirmation_number', None)
    approval_confirm = requests.post(base_url + 'mtnDebitApprovalConfirm', data=json.dumps(data), headers=headers)
    return approval_confirm.json()


def mtn_cash_in(phone_number, amount):
    data = {
        "session_uuid": session_uuid
    }
    data['amount'] = amount
    data['receiving_msisdn'] = phone_number
    data['product_id'] = '1608'
    r = requests.post(base_url + 'mtnCashIn', data=json.dumps(data), headers=headers)
    data['data_reference_number'] = r.json().get('data_reference_number', None)
    data['data'] = phone_number
    submit_data = requests.post(base_url + 'mtnCashInSubmitData', data=json.dumps(data), headers=headers)
    return submit_data.json()


def all1zed_pay_for_bus(customer_phone_number, bus_owner_phone_number, customer_amount, bus_owner_amount):
    print(mtn_debit(customer_phone_number, customer_amount))
    print(mtn_cash_in(bus_owner_phone_number, bus_owner_amount))


def airtel_report():
    default_data['product_id'] = '5393'
    r = requests.post(base_url + 'report', data=json.dumps(default_data), headers=headers)
    return r.json()
