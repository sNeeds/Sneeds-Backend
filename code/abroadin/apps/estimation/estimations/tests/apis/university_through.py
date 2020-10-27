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


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class UniversityThroughModelTests(EstimationsAppAPITests):

    def setUp(self):
        self.local_form1 = StudentDetailedInfo.objects.create()
        super().setUp()

    def test_university_through_get_form_review_200(self):

        def create_university_through(grade, university, gpa):
            university_through = UniversityThrough.objects.create(
                student_detailed_info=self.local_form1,
                university=university,
                grade=grade,
                major=self.major1,
                graduate_in=2018,
                thesis_title="Foo title",
                gpa=gpa
            )
            return university_through

        def create_university_through_with_kwargs(**kwargs):
            multiplied_list_len = 1
            for key in kwargs.keys():
                multiplied_list_len *= len(key)

            multiplied_list = [{} for _ in range(multiplied_list_len)]

            for i, (key, values) in enumerate(kwargs.items()):
                for value in values
                    multiplied_list[i][key] = value


        gpas = [0, 1, 10, 13, 15, 15.5, 17, 17.5, 19, 19.5, 20]
        universities = []
        for rank in [1, 50, 101, 200, 400, 800, 1500, 2000, 5000, 100000]:
            universities.append(University.objects.create(
                name="Foo uni{}".format(rank),
                search_name="Foo uni{}".format(rank),
                country=self.country1,
                rank=rank
            ))

        create_university_through_with_kwargs(gpa=gpas, university=universities, grade=[GradeChoices.BACHELOR])
        # all_grades_subsets = powerset(GradeChoices)
        # for grades in all_grades_subsets:
        #     university_through_list = []
        #     for grade in grades:
        #         create_university_through_with_gpas_universities()
        #
        #         university_through_list.append(create_university_through(grade))
        #
        #     self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_form1.id)
        #     for university_through in university_through_list:
        #         university_through.delete()
