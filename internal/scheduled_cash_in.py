from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from core.kazang import mobile_cash_in
from datetime import datetime, date, time, timedelta

right_now = datetime.now()
today = date.today()

thirty_minutes_before = right_now - timedelta(minutes=30)
in_24_hours = right_now - timedelta(hours=24)
from .models import Transaction

failed_transactions_thirty_minutes = Transaction.objects.filter(date_time_created__gt=thirty_minutes_before,
                                                 status='failed', type='cash_in')
failed_transactions_in_24_hours = Transaction.objects.filter(date_time_created__gt=in_24_hours,
                                                             status='failed', type='cash_in')

@api_view()
def cash_in_30_min(request):
    """
    Redo the cash_in transactions that failed in the previous 3o minutes.
    """
    if failed_transactions_thirty_minutes.exists():
        for transaction in failed_transactions_thirty_minutes:
            cash_in = mobile_cash_in(transaction.phone_number, transaction.amount)
            if cash_in.get('response_code', False) == '0':
                failed_transactions_thirty_minutes.filter(pk=transaction.pk).update(date_time_created=right_now, status='successful')
            else:
                pass
    return Response('Computation done successfully')


# @api_view()
def cash_in_24_hours(request):
    """
    Redo the transactions that failed in the previous 24 hours.
    """
    if failed_transactions_in_24_hours.exists():
        for transaction in failed_transactions_in_24_hours:
           cash_in = mobile_cash_in(transaction.phone_number, transaction.amount)
           if cash_in.get('response_code', False) == '0':
               failed_transactions_in_24_hours.filter(pk=transaction.pk).update(date_time_created=right_now, status='successful')
           else:
               pass
    return Response('Computation done successfully')
