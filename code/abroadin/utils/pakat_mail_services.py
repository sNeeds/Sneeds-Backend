import requests
import json

from django.conf import settings

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'api-key': settings.PAKAT_API_KEY,
}


WEBSITE_LIST = 27
MY_DESTINATION_CAMPAIGN_LIST = 40
SUBSCRIBE_DOI_LIST = 29


def pakat_appropriate_lists(user):
    lists = [WEBSITE_LIST]
    if user.receive_marketing_email:
        lists.append(SUBSCRIBE_DOI_LIST)
    return lists


def send_verification_code_email(send_to, full_name, code):
    url = "https://api.pakat.net/v3/smtp/email"

    if code is None or len(code) == 0:
        raise Exception("Code is None or empty string")

    params = {"verification_code": code,
              "full_name": full_name,
              'full_name_exists': True if full_name is not None and len(full_name) > 2 else False}

    payload = {
        "sender": {"name": "abroadin", "email": 'marketing@abroadin.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'abroadin.marketing@gmail.com'},
        "params": params,
        "templateId": 66,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_reset_password_email(send_to, full_name, reset_password_link):
    url = "https://api.pakat.net/v3/smtp/email"

    if reset_password_link is None or len(reset_password_link) == 0:
        raise Exception("reset_password_link is None or empty string")

    params = {"reset_password_link": reset_password_link,
              "full_name": full_name,
              'full_name_exists': True if full_name is not None and len(full_name) > 2 else False}
    payload = {
        "sender": {"name": "abroadin", "email": 'marketing@abroadin.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'abroadin.marketing@gmail.com'},
        "params": params,
        "templateId": 71,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def create_pakat_contact(email, *args, **kwargs):
    url = "https://api.pakat.net/v3/contacts"

    payload = {
        "attributes": {'FIRSTNAME': kwargs.get('first_name'),
                       'LASTNAME': kwargs.get('last_name'),
                       'SMS': kwargs.get('phone_number'),
                       'OPT_IN': kwargs.get('opt_in', False),
                       'RECEIVE_MARKETING_EMAIL': kwargs.get('receive_marketing_email', False),
                       },
        "listIds": kwargs.get('lists'),
        "email": email,
        "updateEnabled": True,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def update_pakat_contact(email, *args, **kwargs):
    url = "https://api.pakat.net/v3/contacts/"+str(email)+"/"

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
    print(settings.PAKAT_API_KEY)
    return 'pakat_mail_service_response:' + response.text


def create_pakat_doi_contact(email, *args, **kwargs):
    url = "https://api.pakat.net/v3/contacts/doubleOptinConfirmation"

    attributes = {'FIRSTNAME': kwargs.get('first_name'),
                  'LASTNAME': kwargs.get('last_name')}

    if kwargs.get('phone_number'):
        attributes['SMS'] = kwargs.get('phone_number')

    payload = {
        "attributes": attributes,
        "includeListIds": [SUBSCRIBE_DOI_LIST],
        "templateId": 70,
        "email": email,
        "redirectionUrl": "https://abroadin.com/"
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_email(send_to, mail_template, **params):
    url = "https://api.pakat.net/v3/smtp/email"

    payload = {
        "sender": {"name": "abroadin", "email": 'marketing@abroadin.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'abroadin.marketing@gmail.com'},
        "params": params,
        "templateId": mail_template,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_order_created_email(send_to, name, order_url):
    url = "https://api.sendinblue.com/v3/smtp/email"

    payload = {
        "sender": {"name": "abroadin", "email": 'marketing@abroadin.com'},
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
