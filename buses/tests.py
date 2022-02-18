from django.test import TestCase

import requests

params = {'departure_date': '2022-02-14', 'departure_time': '13:18:25', 'bus_short_name': 'matt1'}
r = requests.get('http://localhost:8000/buses/matt1/tickets-sold', params=params)
print(r.status_code)
