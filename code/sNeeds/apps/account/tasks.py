from celery import shared_task
from django.db.models import F

from sNeeds.apps.account.models import StudentDetailedInfo


@shared_task
def update_student_detailed_info_ranks(exclude_id):
    student_detailed_info_qs = StudentDetailedInfo.objects.all().exclude(id=exclude_id)
    student_detailed_info_tuples_list = student_detailed_info_qs.get_with_value_rank_list()

    for t in student_detailed_info_tuples_list:
        obj = t[0]
        rank = t[1]

        obj.rank = rank
        obj.save()


@shared_task
def add_one_to_rank_with_values_greater_than_this(value, exclude_id):
    student_detailed_info_qs = StudentDetailedInfo.objects.filter(value__lt=value).exclude(id=exclude_id)
    student_detailed_info_qs.add_one_to_rank()
