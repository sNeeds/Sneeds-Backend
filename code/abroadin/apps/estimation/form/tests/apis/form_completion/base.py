from rest_framework import status
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model

User = get_user_model()


class FormCompletionBaseTestsMixin:
    include_in_test = False

    def setUp(self) -> None:
        super().setUp()

    def _fc_mixin_endpoint_method(self, *args, **kwargs):
        raise NotImplementedError

    def test_completed_form_get_200(self):
        if not self.include_in_test:
            return
        self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_incomplete_form_educations_get_charts_400(self):
        if not self.include_in_test:
            return
        self.student_detailed_info1.educations.all().delete()
        data = self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.student_detailed_info1.id
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
        self.student_detailed_info1.want_to_apply.delete()
        data = self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.student_detailed_info1.id
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
        self.student_detailed_info1.want_to_apply.countries.set([])
        data = self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.student_detailed_info1.id
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
        self.student_detailed_info1.want_to_apply.grades.set([])
        data = self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.student_detailed_info1.id
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
        self.student_detailed_info1.want_to_apply.semester_years.set([])
        data = self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.student_detailed_info1.id
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
        self.student_detailed_info1.want_to_apply.universities.set([])
        data = self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_incomplete_form_want_to_apply_no_majors_get_charts_200(self):
        if not self.include_in_test:
            return
        self.student_detailed_info1.want_to_apply.majors.set([])
        data = self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_incomplete_form_no_is_married_want_to_apply_no_countries_get_charts_400(self):
        if not self.include_in_test:
            return
        self.student_detailed_info1.want_to_apply.countries.set([])
        self.student_detailed_info1.is_married = None
        self.student_detailed_info1.save()
        data = self._fc_mixin_endpoint_method(
            'get', self.user1, status.HTTP_400_BAD_REQUEST, reverse_args=self.student_detailed_info1.id
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
