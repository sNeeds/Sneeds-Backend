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



from abroadin.apps.estimation.form.models import StudentDetailedInfoBase, StudentDetailedInfo
from abroadin.apps.data.applydata.models import Education
from django.contrib.contenttypes.models import ContentType

StudentDetailedInfoBase.objects.get(id=711).educations_to_base.all()
StudentDetailedInfo.objects.get(id=711).educations.all()

Education.objects.filter(student_detailed_info__studentdetailedinfobase_ptr=711)
Education.objects.filter(student_detailed_info__studentdetailedinfobase_ptr_id=711)
Education.objects.filter(student_detailed_info__studentdetailedinfobase_ptr__id=711)

sdi_ct = ContentType.objects.get_for_model(StudentDetailedInfo)
Education.objects.filter(content_type=sdi_ct, object_id=711)
Education.objects.filter(student_detailed_info__gender='Male')