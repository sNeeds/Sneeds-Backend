import json

import requests

data = {
    "email": "akbar@gmail.com",
    "password": "aaaaaa"
}
r = requests.post('http://127.0.0.1:8000/users/auth/jwt/token/', data=data)

print()
token = json.loads(r.text)["access"]

headers = {"Authorization": "Bearer " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA4MjM4Mzc0LCJqdGkiOiI0NDAxNmZiNjJkMmI0Mzg1YmU2Yzg0OTgzZTAwYTA4ZiIsInVzZXJfaWQiOjI0OH0.36qGCOZUvZGz02BdFogs2iYKnYVauypp_8b3ShK11u4"}
r = requests.get('http://127.0.0.1:8000/users/auth/my-account/', headers=headers)
print(r.text)
