from django.db import models
from django.utils import timezone

from abroadin.base.mixins.validators import CreateM2MManagerMixin
from .variables import FORM_WITHOUT_USER_LIVE_PERIOD_DAYS


def get_grade_or_none(self, grade):
    try:
        return self.all().get(grade=grade)
    except self.model.DoesNotExist:
        return None


class StudentDetailedInfoManager(models.QuerySet):
    def get_with_value_rank_list(self):
        result = []

        rank = 1
        counter = 0
        prev = self.first()

        for obj in self.all().order_by('-value'):
            counter += 1
            if obj.value != prev.value:
                rank = counter
            prev = obj
            result.append((obj, rank))

        return result

    def add_one_to_rank(self):
        for obj in self.all():
            obj.rank += 1
            obj.save()

    def delete_forms_without_user(self, live_period=None):
        if not live_period:
            live_period = FORM_WITHOUT_USER_LIVE_PERIOD_DAYS
        deadline = timezone.now() - timezone.timedelta(days=live_period)
        qs = self.all().filter(created__lt=deadline, user__isnull=True)
        return qs.delete()


class WantToApplyManager(CreateM2MManagerMixin, models.QuerySet):
    pass
