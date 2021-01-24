import json
import time

import requests

data = {
    "certificate_type": "applydata__regularlanguagecertificate",

}
r = requests.post('http://127.0.0.1:8000/analyze/form/ali/', data=data)

print(r.text)
