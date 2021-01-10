from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.tests.base import EstimationBaseTest
from abroadin.apps.estimation.form.models import StudentDetailedInfo, Grade, WantToApply, SemesterYear, \
    Education, GradeChoices, Publication, RegularLanguageCertificate, LanguageCertificate
from abroadin.apps.data.account.models import Country, University, Major
from abroadin.apps.estimation.similarApply.models import AppliedStudentDetailedInfo, AppliedTo

User = get_user_model()


class SimilarApplyAppBaseTests(EstimationBaseTest):

    def setUp(self):
        super().setUp()

        self.app_form_1 = StudentDetailedInfo.objects.create(
            user=self.user1,
        )

        self.app_form_1_university_through_1 = Education.objects.create(
            student_detailed_info=self.app_form_1,
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major1,
            graduate_in=2021,
            thesis_title="Foo thesis",
            gpa=17
        )

        self.app_form_1_university_through_2 = Education.objects.create(
            student_detailed_info=self.app_form_1,
            university=self.university2,
            grade=GradeChoices.MASTER,
            major=self.major1,
            graduate_in=2024,
            thesis_title="Foo thesis",
            gpa=17.5
        )

        self.app_form_1_want_to_apply = WantToApply.objects.create(
            student_detailed_info=self.app_form_1,
        )
        self.app_form_1_want_to_apply.countries.set(
            Country.objects.filter(id__in=[self.country1.id, self.country2.id]),
        )
        self.app_form_1_want_to_apply.universities.set(
            University.objects.filter(id__in=[self.university1.id, ]),
        )
        self.app_form_1_want_to_apply.grades.set(
            Grade.objects.filter(id__in=[Grade.objects.get(name=GradeChoices.PHD).id]),
        )
        self.app_form_1_want_to_apply.majors.set(
            Major.objects.filter(id__in=[self.major1.id, self.major2.id])
        )
        self.app_form_1_want_to_apply.semester_years.set(
            SemesterYear.objects.filter(id__in=[self.semester_year1.id, self.semester_year2.id])
        )

        # Applied student 1

        self.app_applied_student_form_1 = AppliedStudentDetailedInfo.objects.create(
            student_name="Foo student2",
        )

    def create_applied_to(self, form, university, grade, major):
        obj = AppliedTo.objects.create(
            applied_student_detailed_info=form,
            university=university,
            grade=grade,
            major=major,
            semester_year=self.semester_year2,
            fund=20000,
            accepted=True,
            comment="Foo comment"
        )
        return obj
