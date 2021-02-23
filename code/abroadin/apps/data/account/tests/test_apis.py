from rest_framework.test import APITestCase, APIClient

from abroadin.apps.data.account.models import Major, University, Country

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.form.models import StudentDetailedInfo

User = get_user_model()


class StudentDetailedInfoTests(APITestCase):

    def setUp(self):
        # Users -------
        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234")
        self.user1.is_admin = False
        self.user1.set_user_type_student()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234")
        self.user2.is_admin = False
        self.user2.set_user_type_student()

        # Countries -------
        self.country1 = Country.objects.create(
            name="country1",
            slug="country1",
            picture=None
        )

        self.country2 = Country.objects.create(
            name="country2",
            slug="country2",
            picture=None
        )

        # Universities -------
        self.university1 = University.objects.create(
            name="university1",
            country=self.country1,
            description="Test desc1",
            picture=None,
            slug="university1"
        )

        self.university2 = University.objects.create(
            name="university2",
            country=self.country2,
            description="Test desc2",
            picture=None,
            slug="university2"
        )

        # Field of Studies -------
        self.major1 = Major.objects.create(
            name="field of study1",
            description="Test desc1",
            picture=None,
            slug="field-of-study1"
        )

        self.major2 = Major.objects.create(
            name="field of study2",
            description="Test desc2",
            picture=None,
            slug="field-of-study2"
        )

        payload = {
            "user": self.user1,
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 50,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }
        self.student_detailed_info1 = StudentDetailedInfo.objects.create(**payload)

        self.client = APIClient()

    def test_list_post_success_valid_credentials_set_user_correct(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 50,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user2.id)

    def test_list_post_fail_invalid_marital_status(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "marrlnlnied",
            "grade": "college",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 50,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_post_fail_invalid_grade_status(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "single",
            "grade": "post_doctoral",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 50,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_post_fail_invalid_language_speaking(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "single",
            "grade": "doctoral",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 500,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_multi_student_info_fail(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user1)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "single",
            "grade": "doctoral",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 10,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }
        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_put_patch_delete_denied(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 50,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = client.delete(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_owner_patch_success(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.user1)
        payload = {
            "first_name": "akbar",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
            "university": "payamnoor",
            "total_average": "17.00",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 56,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
        }

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), payload.get("first_name"))
        self.assertEqual(response.data.get("total_average"), payload.get("total_average"))
        self.assertEqual(response.data.get("language_speaking"), payload.get("language_speaking"))

    def test_detail_owner_update_success(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.user1)
        payload = {
            "first_name": "asghar",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
            "university": "payamnoor",
            "total_average": "9.10",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 20,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), payload.get("first_name"))
        self.assertEqual(response.data.get("total_average"), payload.get("total_average"))
        self.assertEqual(response.data.get("language_speaking"), payload.get("language_speaking"))

    def test_detail_patch_change_user_denied(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.user1)
        # print(self.student_detailed_info1.user.id)
        payload = {
            "user": self.user2.id
        }

        response = client.patch(url, payload)
        # print(response.data.get("user"))
        # print(self.student_detailed_info1.user.id)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.student_detailed_info1.user.id, self.user1.id)

    def test_detail_other_users_detail_get_patch_put_fail(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.user2)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        payload = {
            "first_name": "asghar",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
        }

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
