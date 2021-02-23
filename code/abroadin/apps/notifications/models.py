import json
from jsonfield import JSONField

from django.db import models


class Notification(models.Model):
    send_date = models.DateTimeField()
    sent = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class EmailNotification(Notification):
    email = models.EmailField()
    data_json = JSONField()

    def get_data_dict(self):
        return json.loads(self.data_json)
