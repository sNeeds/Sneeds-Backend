import requests
import json

from django.conf import settings

url = "https://api.sendinblue.com/v3/smtp/email"

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'api-key': settings.SENDINBLUE_API_KEY
}


def reset_password(send_to, name, resetlink):
    payload = {
        "sender": {"name": "abroadin", "email": 'noreply.abroadin@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.abroadin@gmail.com'},
        "params": {"name": name, "resetlink": resetlink},
        "templateId": 5,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_order_created_email(send_to, name, order_url):
    payload = {
        "sender": {"name": "abroadin", "email": 'noreply.abroadin@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.abroadin@gmail.com'},
        "params": {"name": name, "order_url": order_url},
        "templateId": 6,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_sold_time_slot_email(send_to, name, sold_time_slot_url, start_time, end_time):
    payload = {
        "sender": {"name": "abroadin", "email": 'noreply.abroadin@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.abroadin@gmail.com'},
        "params": {
            "name": name,
            "sold_time_slot_url": sold_time_slot_url,
            "start_time": start_time,
            "end_time": end_time,
        },
        "templateId": 7,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_sold_time_slot_start_reminder_email(send_to, name, sold_time_slot_url, start_time, end_time):
    payload = {
        "sender": {"name": "abroadin", "email": 'noreply.abroadin@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.abroadin@gmail.com'},
        "params": {
            "name": name,
            "sold_time_slot_url": sold_time_slot_url,
            "start_time": start_time,
            "end_time": end_time,
        },
        "templateId": 8,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_sold_time_slot_changed_email(send_to, name, sold_time_slot_url, start_time, end_time):
    payload = {
        "sender": {"name": "abroadin", "email": 'noreply.abroadin@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.abroadin@gmail.com'},
        "params": {
            "name": name,
            "sold_time_slot_url": sold_time_slot_url,
            "start_time": start_time,
            "end_time": end_time,
        },
        "templateId": 9,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_verification_code_email(send_to, full_name, code):
    if code is None or len(code) == 0:
        raise Exception("Code is None or empty string")

    params = {"verification_code": code,
              "full_name": full_name,
              'full_name_exists': True if full_name is not None and len(full_name) > 2 else False}

    payload = {
        "sender": {"name": "abroadin", "email": 'abroadin.dev@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'abroadin.dev@gmail.com'},
        "params": params,
        "templateId": 1,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text
