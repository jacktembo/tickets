import requests
import json

url = 'https://probasesms.com/api/json/multi/res/bulk/sms'

params = {
    'senderid': 'All1Zed', 'username': 'All1Zed@12$$', 'password': 'All1Zed@sms12$$',
    'recipient': ['260971977252'],
    'message': 'Welcome Jack'
}
r = requests.post(url, data=params)
print(r.json())

