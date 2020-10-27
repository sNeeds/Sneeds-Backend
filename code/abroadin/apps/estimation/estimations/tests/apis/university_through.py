import uuid
from itertools import chain, combinations

from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.account.models import Country, University, Major
from apps.estimation.estimations.tests.apis.base import EstimationsAppAPITests
from apps.estimation.estimations.tests.models.base import EstimationsAppModelTests
from abroadin.apps.estimation.form.models import (
    StudentDetailedInfo,
    Grade,
    WantToApply,
    SemesterYear,
    UniversityThrough,
    GradeChoices,
    Publication,
    RegularLanguageCertificate,
    LanguageCertificate
)

User = get_user_model()


class UniversityThroughAPITests(EstimationsAppAPITests):

    def setUp(self):
        self.local_form1 = StudentDetailedInfo.objects.create()
        super().setUp()

    def test_university_through_get_form_review_200_1(self):
        gpas = [0, 1, 10, 13, 15, 15.5, 17, 17.5, 19, 19.5, 20]
        ranks = [1, 50, 101, 200, 400, 800, 1500, 2000, 5000, 100000]

        for gpa in gpas:
            for rank in ranks:
                university = University.objects.create(
                    name="Foo uni{}".format(rank),
                    search_name="Foo uni{}".format(rank),
                    country=self.country1,
                    rank=rank
                )

                university_through = UniversityThrough.objects.create(
                    student_detailed_info=self.local_form1,
                    university=university,
                    grade=GradeChoices.BACHELOR,
                    major=self.major1,
                    graduate_in=2018,
                    thesis_title="Foo title",
                    gpa=gpa
                )
                university_through.delete()
                university.delete()

                self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_form1.id)

    def test_university_through_get_form_review_200_2(self):
        for grade in GradeChoices:
            UniversityThrough.objects.create(
                student_detailed_info=self.local_form1,
                university=self.university1,
                grade=grade,
                major=self.major1,
                graduate_in=2018,
                thesis_title="Foo title",
                gpa=18
            )
            self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_form1.id)
