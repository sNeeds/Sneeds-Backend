from django.db import models

from sNeeds.apps.users.account.models import StudentDetailedInfoBase, Country, University, GradeModel, FieldOfStudy, \
    StudentFormApplySemesterYear
from sNeeds.apps.estimation.similarApply.managers import AppliedStudentDetailedInfoQuerySetManager


class AppliedTo(models.Model):
    applied_student_detailed_info = models.ForeignKey(
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
