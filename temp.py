import json
import time

import requests

data = {
    "certificate_type": "applydata__regularlanguagecertificate",
    "data": {
        "reading": 5,
        "listening": 5,
        "speaking": 5,
        "writing": 5,
        "overall": 5,
        "certificate_type": "sdsd",  # TODO: Check works
        "is_mock": False
    }
}

r = requests.post('http://127.0.0.1:8000/analyze/form/ali/', json=data)

print(r.text)
