import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token b1136fb60f5b0484cac2827b8642b55b6f2e517a'
}

url2 = 'https://buses.all1zed.com/cash-in-24-hours'
r2 = requests.get(url2, headers=headers)
print(r2.text)
