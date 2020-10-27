from __future__ import print_function

import json

import requests


url = "https://api.sendinblue.com/v3/smtp/email"

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'api-key': "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"
}

payload = {
    "sender": {"name": "abroadin", "email": 'noreply.abroadin@gmail.com'},
    "to": [{"email": "bartararya@gmail.com"}],
    "replyTo": {'email': 'noreply.abroadin@gmail.com'},
    "params": {
    },
    "templateId": 8,
}
json_data = json.dumps(payload)
response = requests.request("POST", url, data=json_data, headers=headers)
print(response.text)
