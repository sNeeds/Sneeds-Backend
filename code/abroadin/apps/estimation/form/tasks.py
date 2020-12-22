import time

from celery import shared_task
from django.db.models import F

from django.conf import settings
from django.utils import timezone

from .models import StudentDetailedInfo


# TODO: Change logic
@shared_task
def update_student_detailed_info_ranks():
    student_detailed_info_qs = StudentDetailedInfo.objects.all().order_by("-value")

    for r, obj in enumerate(student_detailed_info_qs):
        StudentDetailedInfo.objects.filter(id=obj.id).update(rank=r + 1)



@shared_task
def add_one_to_rank_with_values_greater_than_this(value, exclude_id):
    student_detailed_info_qs = StudentDetailedInfo.objects.filter(value__lt=value).exclude(id=exclude_id)
    student_detailed_info_qs.add_one_to_rank()


@shared_task()
def delete_forms_without_user(live_period=None):
    StudentDetailedInfo.objects.delete_forms_without_user(live_period=live_period)
