import uuid

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


class UniversityThroughModelTests(EstimationsAppAPITests):

    def setUp(self):
        self.local_form1 = StudentDetailedInfo.objects.create()
        super().setUp()

    def test_university_through_get_form_review_200(self):
        for rank in [1, 50, 101, 200, 400, 800, 1500, 2000, 5000]:
            university = University.objects.create(
                name="Foo uni{}".format(rank),
                search_name="Foo uni{}".format(rank),
                country=self.country1,
                rank=rank
            )
            print()
            for gpa in [1, 10, 14, 15, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20]:
                university_through = UniversityThrough.objects.create(
                    student_detailed_info=self.local_form1,
                    university=university,
                    grade=GradeChoices.BACHELOR,
                    major=self.major1,
                    graduate_in=2018,
                    thesis_title="Foo title",
                    gpa=gpa
                )

                print("rank:", rank, "gpa:", gpa, "value:", university_through.value)
                response = self._test_form_comments_detail("get", None, status.HTTP_200_OK,
                                                           reverse_args=self.local_form1.id)
                # print(
                #     response["university_and_gpa"]["data"]["bachelor"],
                #     "| Label:", response["university_and_gpa"]["value_label"],
                #     "| University Value:", response["university_and_gpa"]["university_value"],
                #     "| GPA Value:", response["university_and_gpa"]["gpa_value"]
                # )
                print(
                    "| Label:", response["university_and_gpa"]["value_label"],
                    "| University Value:", response["university_and_gpa"]["university_value"],
                    "| GPA Value:", response["university_and_gpa"]["gpa_value"]
                )
                university_through.delete()
