from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from sNeeds.apps.account.models import StudentDetailedInfoBase, Country, University, GradeModel, FieldOfStudy, \
    StudentFormApplySemesterYear
from sNeeds.apps.similarApply.managers import AppliedStudentDetailedInfoQuerySetManager


class AppliedTo(models.Model):
    applied_student_detailed_info = models.OneToOneField(
        'AppliedStudentDetailedInfo',
        on_delete=models.CASCADE,
        related_name="applied_to"
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE
    )

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE
    )

    grade = models.ForeignKey(
        GradeModel,
        on_delete=models.CASCADE,
    )

    major = models.ForeignKey(
        FieldOfStudy,
        on_delete=models.CASCADE
    )

    semester_year = models.ForeignKey(
        StudentFormApplySemesterYear,
        on_delete=models.PROTECT
    )

    fund = models.IntegerField(
        help_text="In Dollars"
    )

    accepted = models.BooleanField()

    comment = models.CharField(
        max_length=1024
    )


class AppliedStudentDetailedInfo(StudentDetailedInfoBase):
    objects = AppliedStudentDetailedInfoQuerySetManager.as_manager()
