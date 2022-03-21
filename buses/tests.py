# import requests
# import json
# url = "https://probasesms.com/api/json/multi/res/bulk/sms"
#
# payload = json.dumps({
#     "username": "All1Zed@12$$", "password": "All1Zed@sms12$$",
#     "recipient": [260971977252], "senderid": "All1Zed", "message": "Welcome Jack",
#     "source": "All1Zed"
# })
# headers = {
#     'Content-Type': 'application/json'
# }
#
# response = requests.request("POST", url, headers=headers, data=payload)
# print(response.text)
import json
import requests
data = [{"bus": "fmb1","starting_place": "Zimba","destination": "Livingstone","time": "09:00","price": "280"}]
data = json.dumps(data)
r = requests.post('http://localhost:8000/api/bulk', data=data, headers={'Content-Type': 'application/json'})
print(r.json())
