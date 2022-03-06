import requests
headers = {
    'Authorization': 'Token dc52a962fb73d7a8a08594f0c521923ebfae41c1'
}
r = requests.get('http://localhost:8000/api/bus-companies')
print(r.json())