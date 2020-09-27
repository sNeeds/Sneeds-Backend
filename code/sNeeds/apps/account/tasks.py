from celery import shared_task
from django.db.models import F

from sNeeds.apps.account.models import StudentDetailedInfo


@shared_task
def update_student_detailed_info_ranks():
    student_detailed_info_qs = StudentDetailedInfo.objects.all().order_by('-value')

    counter = 1
    for obj in student_detailed_info_qs:
        obj.rank = counter
        obj.save()