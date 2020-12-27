import time
import sqlparse

from celery import shared_task
from django.db.models import F, Count, Q, OuterRef, Subquery, Value, Case, When, IntegerField

from .models import StudentDetailedInfo, WantToApply


@shared_task
def update_student_detailed_info_ranks():
    ranked_sdi = StudentDetailedInfo.objects.filter(
        value__gt=OuterRef('value')
    ).annotate(
        none=Value(None)
    ).values(
        'none'
    ).annotate(
        count=Count("*")
    ).values('count').order_by('value')

    StudentDetailedInfo.objects.annotate(
        new_rank=Subquery(ranked_sdi)
    ).update(
        rank=Case(
            When(new_rank=0, then=Value(1)),
            default='new_rank',
            output_field=IntegerField(),
        )
    )



@shared_task
def add_one_to_rank_with_values_greater_than_this(value, exclude_id):
    student_detailed_info_qs = StudentDetailedInfo.objects.filter(value__lt=value).exclude(id=exclude_id)
    student_detailed_info_qs.add_one_to_rank()
