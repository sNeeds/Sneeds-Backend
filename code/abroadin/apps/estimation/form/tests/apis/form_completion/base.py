from rest_framework import status
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model

from abroadin.apps.estimation.tests.apis import EstimationBaseTest
from abroadin.apps.estimation.form.models import \
    (StudentDetailedInfo,
     WantToApply,
     UniversityThrough,
     GradeChoices,
     )

User = get_user_model()


class BaseTests(EstimationBaseTest):
    include_in_test = False

    def setUp(self) -> None:

        super().setUp()

        self.completed_sdi_1 = StudentDetailedInfo.objects.create(
            user=self.user1,
            age=27,
            gender=StudentDetailedInfo.GenderChoices.MALE,
            is_married=False,
            payment_affordability=StudentDetailedInfo.PaymentAffordabilityChoices.AVERAGE,
            prefers_full_fund=True,
            prefers_half_fund=True,
            prefers_self_fund=False,
            comment="Foo comment",
            powerful_recommendation=True,
            linkedin_url="https://www.linkedin.com/in/arya-khaligh/",
            homepage_url="http://aryakhaligh.ir/",
        )

        self.sdi_1_university_through_1 = UniversityThrough.objects.create(
            student_detailed_info=self.completed_sdi_1,
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major1,
            graduate_in=2021,
            thesis_title="Foo thesis",
            gpa=17
        )

        self.sdi_1_want_to_apply_1 = WantToApply.objects.create(
            student_detailed_info=self.completed_sdi_1
        )
        self.sdi_1_want_to_apply_1.countries.set([self.country2])
        self.sdi_1_want_to_apply_1.universities.set([self.university2])
        self.sdi_1_want_to_apply_1.semester_years.set([self.semester_year1])
        self.sdi_1_want_to_apply_1.grades.set([self.grade1])
        self.sdi_1_want_to_apply_1.majors.set([self.major1])

    def _endpoint_method(self, *args, **kwargs):
        raise NotImplementedError

    def test_completed_form_get_200(self):
        if not self.include_in_test:
            return
        self._endpoint_method(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.completed_sdi_1.id
        )

    def test_incomplete_form_age_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.age = None
        self.completed_sdi_1.save()
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 1
        )
        self.assertEqual(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], '1',
        )

    def test_incomplete_form_is_married_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.is_married = None
        self.completed_sdi_1.save()
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 1
        )
        self.assertEqual(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], '2',
        )

    def test_incomplete_form_gender_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.gender = None
        self.completed_sdi_1.save()
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 1
        )
        self.assertEqual(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], '3',
        )

    def test_incomplete_form_university_through_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.universities.set([])
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 1
        )
        self.assertEqual(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], '4',
        )

    def test_incomplete_form_no_want_to_apply_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.want_to_apply.delete()
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 1
        )
        self.assertEqual(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], '5',
        )

    def test_incomplete_form_want_to_apply_no_countries_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.want_to_apply.countries.set([])
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 1
        )
        self.assertEqual(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], '5',
        )

    def test_incomplete_form_want_to_apply_no_grades_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.want_to_apply.grades.set([])
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 1
        )
        self.assertEqual(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], '5',
        )

    def test_incomplete_form_want_to_apply_no_semester_years_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.want_to_apply.semester_years.set([])
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 1
        )
        self.assertEqual(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], '5',
        )

    def test_incomplete_form_want_to_apply_no_universities_get_charts_200(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.want_to_apply.universities.set([])
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.completed_sdi_1.id
        )

    def test_incomplete_form_want_to_apply_no_majors_get_charts_200(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.want_to_apply.majors.set([])
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.completed_sdi_1.id
        )

    def test_incomplete_form_no_age_want_to_apply_no_semester_years_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.want_to_apply.semester_years.set([])
        self.completed_sdi_1.age = None
        self.completed_sdi_1.save()
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 2
        )
        expected_ids = ['1', '5']
        self.assertIn(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], expected_ids,
        )
        self.assertIn(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][1]['id'], expected_ids,
        )

    def test_incomplete_form_no_is_married_want_to_apply_no_countries_get_charts_400(self):
        if not self.include_in_test:
            return
        self.completed_sdi_1.want_to_apply.countries.set([])
        self.completed_sdi_1.is_married = None
        self.completed_sdi_1.save()
        data = self._endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.completed_sdi_1.id
        )

        self.assertEqual(
            len(data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form']), 2
        )
        expected_ids = ['2', '5']
        self.assertIn(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][0]['id'], expected_ids,
        )
        self.assertIn(
            data[api_settings.NON_FIELD_ERRORS_KEY]['incomplete_form'][1]['id'], expected_ids,
        )