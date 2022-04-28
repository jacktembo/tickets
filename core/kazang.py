# import requests
# import json
# import django
# from datetime import datetime
# from django.conf import settings
# from .models import KazangSession
# from time import sleep
# from threading import Thread
# import string
# import secrets
#
# now = datetime.now().isoformat()
#
# base_url = "https://api.kazang.net/apimanager/api_rest/v1/"
# prod_username = "8011819587"
# prod_password = "*HJe;PJx6g"
# channel = "PridePayments"
# serial_number = "102.147.160.102"
# time_stamp = now
# auth_data = {
#     "username": prod_username, "password": prod_password, "channel": channel
# }
#
# headers = {
#     "Content-Type": "application/json"
#
# }
#
#
# def auth_client():
#     r = requests.post(base_url + "authClient", data=json.dumps(auth_data), headers=headers)
#     return r.json()
#
#
# def get_new_session_uuid():
#     session_uuid = auth_client().get('session_uuid', False)
#     return session_uuid
#
#
# def get_active_session_uuid():
#     """
#     Used for getting the last saved session uuid from the database.
#     """
#     session = KazangSession.objects.all().last()
#     return session.session_uuid
#
#
# def get_or_create_session_uuid():
#     """
#     Get the current active session id. If it does not exist, creates one and returns it.
#     """
#     db_sessions = KazangSession.objects.all().exists()
#     if db_sessions:
#         db_session = KazangSession.objects.all().last().session_uuid
#         data = {"session_uuid": db_session}
#         products = requests.post(base_url + 'productList', data=json.dumps(data), headers=headers)
#         if products.json().get('response_code', False) == 0:
#             return db_session
#         else:
#             session_uuid = get_new_session_uuid()
#             KazangSession.objects.create(session_uuid=session_uuid)
#             return session_uuid
#     else:
#         session_uuid = get_new_session_uuid()
#         KazangSession.objects.create(session_uuid=session_uuid)
#         return session_uuid
#
#
# session_uuid = get_or_create_session_uuid()
#
#
# def get_balance():
#     return product_list().get('balance', None)
#
#
# def is_session_active(response):
#     return response.json().get('response_code', False) == 0
#
#
# data = {
#     "session_uuid": session_uuid
# }
# default_data = {
#     'session_uuid': session_uuid
# }
#
# def product_list():
#     default_data = {
#         'session_uuid': session_uuid
#     }
#     r = requests.post(base_url + 'productList', data=json.dumps(data), headers=headers)
#     products = r.json().get('product_list', None)
#     return products
#
#
# def find_product_from_method_name(method: str):
#     """
#     Get a product dictionary form an API method name
#     :param method:
#     :return dict:
#     """
#     products = product_list()
#     return next(item for item in products if item["method_name"] == method)
#
#
# def airtel_pay_payment(phone_number: str, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     code3 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     """
#     Airtel Pay Payment step 1.
#     :param phone_number:
#     :param amount:
#     :return:
#     """
#     data['product_id'] = find_product_from_method_name('airtelPayPayment')['product_id']
#     data['wallet_msisdn'] = phone_number
#     data['amount'] = amount
#     r = requests.post(base_url + "airtelPayPayment", data=json.dumps(data), headers=headers)
#     confirmation_number = r.json().get('confirmation_number', False)
#     data['confirmation_number'] = confirmation_number
#     confirm = requests.post(base_url + "airtelPayPaymentConfirm", data=json.dumps(data), headers=headers)
#     return confirm.json()
#
#
# def airtel_pay_query(phone_number, amount, airtel_reference):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     code3 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data['airtel_reference'] = airtel_reference
#     data['product_id'] = find_product_from_method_name('airtelPayQuery')['product_id']
#     data['wallet_msisdn'] = phone_number
#     data['amount'] = amount
#     airtel_pay_query = requests.post(base_url + "airtelPayQuery", data=json.dumps(data), headers=headers)
#     data['confirmation_number'] = airtel_pay_query.json().get('confirmation_number', False)
#     airtel_pay_query_confirm = requests.post(base_url + "airtelPayQueryConfirm", data=json.dumps(data), headers=headers)
#
#     return airtel_pay_query_confirm.json()
#
#
# def zamtel_money_pay(phone_number: str, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     code3 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     """Zamtel Money Pay workflow"""
#     data['request_reference'] = code
#     data['msisdn'] = phone_number
#     data['amount'] = amount
#     data['product_id'] = find_product_from_method_name('zamtelMoneyPay')['product_id']
#     zamtel_money_pay = requests.post(base_url + 'zamtelMoneyPay', data=json.dumps(data), headers=headers)
#     return zamtel_money_pay.json()
#
#
# def zamtel_money_pay_confirm(phone_number, amount, confirmation_number):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data['request_reference'] = code
#     data['confirmation_number'] = confirmation_number
#     data['request_reference'] = code2
#     data['msisdn'] = phone_number
#     data['amount'] = amount
#     zamtel_pay_confirmation = requests.post(base_url + 'zamtelMoneyPayConfirm', data=json.dumps(data), headers=headers)
#     return zamtel_pay_confirmation.json()
#
#
# def mtn_debit(phone_number: str, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data['request_reference'] = code2
#     data['wallet_msisdn'] = phone_number
#     data['amount'] = amount
#     data['product_id'] = find_product_from_method_name('mtnDebit')['product_id']
#     r = requests.post(base_url + 'mtnDebit', data=json.dumps(data), headers=headers)
#     return r.json()
#
#
# def mtn_debit_confirm(phone_number, amount, confirmation_number):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data['request_reference'] = code
#     data['supplier_transaction_id'] = confirmation_number
#     data['wallet_msisdn'] = phone_number
#     data['amount'] = amount
#     data['product_id'] = find_product_from_method_name('mtnDebitCnfirm')['product_id']
#     approval = requests.post(base_url + 'mtnDebitApproval', data=json.dumps(data), headers=headers)
#     data['confirmation_number'] = approval.json().get('confirmation_number', None)
#     approval_confirm = requests.post(base_url + 'mtnDebitApprovalConfirm', data=json.dumps(data), headers=headers)
#     return approval_confirm.json()
#
#
# def all1zed_pay_for_bus(customer_phone_number, bus_owner_phone_number, customer_amount, bus_owner_amount):
#     print(mtn_debit(customer_phone_number, customer_amount))
#     print(mtn_cash_in(bus_owner_phone_number, bus_owner_amount))
#
#
# def nfs_cash_in(phone_number, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     data['product_id'] = '1648'
#     data['request_reference'] = code
#     data['reference'] = phone_number
#     data['amount'] = amount
#     cash_in = requests.post(base_url + 'nfsCashIn', data=json.dumps(data), headers=headers)
#     data['confirmation_number'] = cash_in.json().get('confirmation_number', False)
#     data['request_reference'] = code2
#     del data['amount']
#     del data['reference']
#     nfs_cash_in_confirm = requests.post(base_url + 'nfsCashInConfirm', data=json.dumps(data), headers=headers)
#     return  nfs_cash_in_confirm.json()
#
#
# def nfs_cash_out(phone_number, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     data['product_id'] = ''
#     data['request_reference'] = code
#     data['reference'] = phone_number
#     data['amount'] = amount
#     cash_out = requests.post(base_url + 'nfsATMCashOut', data=json.dumps(data), headers=headers)
#     data['data'] = '2020'
#     data['data_reference_number'] = cash_out.json().get('data_reference_number', False)
#     data['request_reference'] = code2
#     del data['amount']
#     del data['reference']
#     cash_out_confirm = requests.post(base_url + 'nfsATMCashOutSubmitData', data=json.dumps(data), headers=headers)
#     return cash_out_confirm.json()
#
#
# def mtn_cash_in(phone_number, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     data['receiving_msisdn'] = phone_number
#     data['amount'] = amount
#     data['product_id'] = find_product_from_method_name('mtnCashIn')['product_id']
#     data['request_reference'] = code
#     cash_in = requests.post(base_url + 'mtnCashIn', data=json.dumps(data), headers=headers)
#     data['data_reference_number'] = cash_in.json().get('data_reference_number', False)
#     data['request_reference'] = code2
#     data['data'] = phone_number
#     del data['receiving_msisdn']
#     del data['amount']
#     cash_in_confirm = requests.post(base_url + 'mtnCashInSubmitData', data=json.dumps(data), headers=headers)
#     return cash_in_confirm.json()
#
#
# def zamtel_money_cash_in(phone_number, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     data['product_id'] = find_product_from_method_name('zamtelMoneyCashIn')['product_id']
#     data['request_reference'] = code
#     data['msisdn'] = phone_number
#     data['amount'] = amount
#     cash_in = requests.post(base_url + 'zamtelMoneyCashIn', data=json.dumps(data), headers=headers)
#     data['confirmation_number'] = cash_in.json().get('confirmation_number', False)
#     data['request_reference'] = code2
#     del data['msisdn']
#     del data['amount']
#     cash_in_confirm = requests.post(base_url + 'zamtelMoneyCashInConfirm', data=json.dumps(data), headers=headers)
#     return cash_in_confirm.json()
#
#
# def direct_recharge_airtime(phone_number, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     data['product_id'] = '1356'
#     data['request_reference'] = code
#     data['msisdn'] = phone_number
#     data['amount'] = amount
#     direct_recharge = requests.post(base_url + 'directRechargeAirtime', data=json.dumps(data), headers=headers)
#     return direct_recharge.json()
#
#
# def direct_recharge_data(phone_number, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     data['request_reference'] = code
#     data['amount'] = amount
#     data['product_id'] = '1357'
#     direct_recharge = requests.post(base_url + 'directRechargeData', data=json.dumps(data), headers=headers)
#     data['confirmation_number'] = direct_recharge.json().get('confirmation_number', False)
#     direct_recharge_confirm = requests.post(base_url + 'confirm', data=json.dumps(data), headers=headers)
#     return direct_recharge_confirm.json()
#
#
# def mtn_cash_out(phone_number, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     code3 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     data['product_id'] = find_product_from_method_name('mtnCashOut')['product_id']
#     data['request_reference'] = code
#     data['receiving_msisdn'] = phone_number
#     data['amount'] = amount
#     cash_out = requests.post(base_url + 'mtnCashOut', data=json.dumps(data), headers=headers)
#     data['supplier_transaction_id'] = cash_out.json().get('supplier_transaction_id', False)
#     data['request_reference'] = code2
#     data['product_id'] = find_product_from_method_name('mtnCashOutApproval')['product_id']
#     cash_out_approval = requests.post(base_url + 'mtnCashOutApproval', data=json.dumps(data), headers=headers)
#     data['confirmation_number'] = cash_out_approval.json().get('confirmation_number', False)
#     data['request_reference'] = code3
#     cash_out_confirm = requests.post(base_url + 'mtnCashOutApprovalConfirm', data=json.dumps(data), headers=headers)
#     return cash_out_confirm.json()
#
#
# def zamtel_money_cash_out(phone_number, amount):
#     alphabet = string.digits
#     code = ''.join(secrets.choice(alphabet) for i in range(6))
#     code2 = ''.join(secrets.choice(alphabet) for i in range(6))
#     code3 = ''.join(secrets.choice(alphabet) for i in range(6))
#     data = {
#         "session_uuid": session_uuid
#     }
#     data['product_id'] = find_product_from_method_name('zamtelMoneyCashOut')['product_id']
#     data['request_reference'] = code
#     data['msisdn'] = phone_number
#     data['amount'] = amount
#     cash_out = requests.post(base_url + 'zamtelMoneyCashOut', data=json.dumps(data), headers=headers)
#     data['confirmation_number'] = cash_out.json().get('confirmation_number', False)
#     data['request_reference'] = code2
#     del data['msisdn']
#     del data['amount']
#     cash_out_confirm = requests.post(base_url + 'zamtelMoneyCashOutConfirm', data=json.dumps(data), headers=headers)
#     return cash_out_confirm.json()
