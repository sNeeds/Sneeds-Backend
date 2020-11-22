import requests
import json

from django.conf import settings

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'api-key': settings.SENDINBLUE_API_KEY
}

MARKETING_LIST = 3
DOI_LIST = 4


def perform_appropriate_lists(user):
    lists = []
    if user.receive_marketing_email:
        lists.append(MARKETING_LIST)
    return lists


def send_verification_code_email(send_to, full_name, code):
    url = "https://api.sendinblue.com/v3/smtp/email"

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


def send_reset_password_email(send_to, full_name, reset_password_link):
    url = "https://api.sendinblue.com/v3/smtp/email"

    if reset_password_link is None or len(reset_password_link) == 0:
        raise Exception("reset_password_link is None or empty string")

    params = {"reset_password_link": reset_password_link,
              "full_name": full_name,
              'full_name_exists': True if full_name is not None and len(full_name) > 2 else False}
    payload = {
        "sender": {"name": "abroadin", "email": 'abroadin.dev@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'abroadin.dev@gmail.com'},
        "params": params,
        "templateId": 3,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def create_sib_contact(email, *args, **kwargs):
    url = "https://api.sendinblue.com/v3/contacts"

    payload = {
        "attributes": {'FIRSTNAME': kwargs.get('first_name'),
                       'LASTNAME': kwargs.get('last_name'),
                       'SMS': kwargs.get('phone_number'),
                       'OPT_IN': kwargs.get('opt_in', False),
                       'RECEIVE_MARKETING_EMAIL': kwargs.get('receive_marketing_email', False),
                       },
        "listIds": kwargs.get('lists'),
        "email": email,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def update_sib_contact(email, *args, **kwargs):
    url = "https://api.sendinblue.com/v3/contacts/"+str(email)+"/"

    payload = {
        "attributes": {'FIRSTNAME': kwargs.get('first_name'),
                       'LASTNAME': kwargs.get('last_name'),
                       'SMS': kwargs.get('phone_number'),
                       'OPT_IN': kwargs.get('opt_in', False),
                       'RECEIVE_MARKETING_EMAIL': kwargs.get('receive_marketing_email', False),
                       },
        "listIds": kwargs.get('lists'),
        "email": email,
    }
    json_data = json.dumps(payload)
    response = requests.request("PUT", url, data=json_data, headers=headers)
    print(response.text)
    return response.text


def create_sib_doi_contact(email, *args, **kwargs):
    url = "https://api.sendinblue.com/v3/contacts/doubleOptinConfirmation"

    attributes = {'FIRSTNAME': kwargs.get('first_name'),
                  'LASTNAME': kwargs.get('last_name')}

    if kwargs.get('phone_number'):
        attributes['SMS'] = kwargs.get('phone_number')

    payload = {
        "attributes": attributes,
        "includeListIds": [3],
        "templateId": 5,
        "email": email,
        "redirectionUrl": "https://abroadin.com/"
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_order_created_email(send_to, name, order_url):
    url = "https://api.sendinblue.com/v3/smtp/email"

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
    url = "https://api.sendinblue.com/v3/smtp/email"

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
    url = "https://api.sendinblue.com/v3/smtp/email"

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
    url = "https://api.sendinblue.com/v3/smtp/email"
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
