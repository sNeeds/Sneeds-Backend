import json
import time

import requests

data = {
    "email": "akbar@gmail.com",
    "password": "aaaaaa"
}
r = requests.post('http://127.0.0.1:8000/users/auth/jwt/token/', data=data)

print(r.text)
token = json.loads(r.text)["access"]

time.sleep(30)
headers = {"Authorization": "Bearer " + token}
r = requests.get('http://127.0.0.1:8000/users/auth/my-account/', headers=headers)
print(r.text)
