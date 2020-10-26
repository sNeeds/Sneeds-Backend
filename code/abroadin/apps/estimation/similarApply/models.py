from django.db import models

from abroadin.apps.data.account.models import Country, University, Major
from abroadin.apps.estimation.form.models import SemesterYear, StudentDetailedInfoBase, GradeChoices
from abroadin.apps.estimation.similarApply.managers import AppliedStudentDetailedInfoQuerySetManager


class AppliedTo(models.Model):
    applied_student_detailed_info = models.ForeignKey(
        'AppliedStudentDetailedInfo',
        on_delete=models.CASCADE,
        related_name="applied_to"
    )
    student_name = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE
    )

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE
    )

    grade = models.CharField(
        max_length=128,
        choices=GradeChoices.choices,
        default=GradeChoices.BACHELOR
    )

    major = models.ForeignKey(
        Major,
        on_delete=models.CASCADE
    )

    semester_year = models.ForeignKey(
        SemesterYear,
        on_delete=models.PROTECT
    )

    fund = models.IntegerField(
        help_text="In Dollars",
        null=True,
        blank=True
    )

    accepted = models.BooleanField()

    comment = models.CharField(
        max_length=1024,
        null=True,
        blank=True
    )


class AppliedStudentDetailedInfo(StudentDetailedInfoBase):
    objects = AppliedStudentDetailedInfoQuerySetManager.as_manager()

    def _applied_to_has_this_major(self, major):
        return AppliedTo.objects.filter(
            applied_student_detailed_info__id=self.id,
            major=major
        ).exists()

    def applied_to_has_these_majors(self, majors_list):
        found = False
        for major in majors_list:
            found = found or self._applied_to_has_this_major(major)
        return found

    def _applied_to_has_this_university(self, university):
        return AppliedTo.objects.filter(
            applied_student_detailed_info__id=self.id,
            university=university
        ).exists()

    def applied_to_has_these_universities(self, universities_list):
        found = False
        for university in universities_list:
            found = found or self._applied_to_has_this_university(university)
        return found
