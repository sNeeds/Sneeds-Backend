from rest_framework.test import APITestCase

from .base import ApplyProfileModelsTestBase
from ...models import ApplyProfile, Admission


class ApplyProfileModelTests(ApplyProfileModelsTestBase, APITestCase):

    def setUp(self) -> None:
        return super(ApplyProfileModelsTestBase, self).setUp()

    def test_apply_profile_creation_correct(self):
        ap = ApplyProfile.objects.create(
            name='sample name',
            gap=6,
        )
        ap.refresh_from_db()
        self.assertEqual(ap.name, 'sample name')
        self.assertEqual(ap.gap, 6)

    def test_apply_profile_set_publications_correct(self):
        ap = ApplyProfile.objects.create(
            name='sample name',
            gap=6,
        )

        self.publication1.content_object = ap
        self.publication1.save()

        self.publication2.content_object = ap
        self.publication2.save()

        self.assertEqual(ap.publications.count(), 2)

    def test_apply_profile_set_educations_correct(self):
        ap = ApplyProfile.objects.create(
            name='sample name',
            gap=6,
        )

        self.education1.content_object = ap
        self.education1.save()

        self.assertNotEqual(self.education1.grade, self.education2.grade)

        self.education2.content_object = ap
        self.education2.save()

        self.assertEqual(ap.educations.count(), 2)

    def test_apply_profile_set_educations_correct_2(self):
        ap = ApplyProfile.objects.create(
            name='sample name',
            gap=6,
        )

        self.education1.content_object = ap
        self.education1.save()

        self.assertEqual(self.education1.grade, self.education4.grade)

        self.education4.content_object = ap
        self.education4.save()

        self.assertEqual(ap.educations.count(), 2)

    def test_apply_profile_set_language_certificates_correct(self):
        ap = ApplyProfile.objects.create(
            name='sample name',
            gap=6,
        )

        self.gre1.content_object = ap
        self.gre1.save()

        self.assertNotEqual(self.gre1.certificate_type, self.ielts1.certificate_type)

        self.ielts1.content_object = ap
        self.ielts1.save()

        self.assertEqual(ap.language_certificates.count(), 2)

    def test_apply_profile_set_language_certificates_incorrect(self):
        ap = ApplyProfile.objects.create(
            name='sample name',
            gap=6,
        )

        self.ielts2.content_object = ap
        self.ielts2.save()

        self.assertEqual(self.ielts2.certificate_type, self.ielts3.certificate_type)

        try:
            self.ielts3.content_object = ap
            self.ielts3.save()
        except Exception as e:
            pass

        self.assertEqual(ap.language_certificates.count(), 1)

    def test_last_education(self):
        ap = ApplyProfile.objects.create(
            name='sample name',
            gap=6,
        )

        self.education1.content_object = ap
        self.education1.save()

        self.assertNotEqual(self.education1.grade, self.education2.grade)

        self.education2.content_object = ap
        self.education2.save()

        self.assertEqual(ap.last_education().id, self.education2.id)

    def test_main_admission(self):
        ap = ApplyProfile.objects.create(
            name='sample name',
            gap=6,
        )

        admission1 = Admission.objects.create(
            grade=self.bachelor_grade,
            destination=self.university1,

            apply_profile=ap,
            major=self.major1,
            accepted=True,
            scholarship=1000,
            enroll_year=2018,
            description="""
                    Some very very good description"""
        )

        admission2 = Admission.objects.create(
            grade=self.bachelor_grade,
            destination=self.university2,

            apply_profile=ap,
            major=self.major1,
            accepted=True,
            scholarship=1000,
            enroll_year=2018,
            description="""
                            Some very very good description"""
        )

        admission3 = Admission.objects.create(
            grade=self.master_grade,
            destination=self.university1,

            apply_profile=ap,
            major=self.major1,
            accepted=True,
            scholarship=1000,
            enroll_year=2018,
            description="""
                            Some very very good description"""
        )

        admission4 = Admission.objects.create(
            grade=self.master_grade,
            destination=self.university2,

            apply_profile=ap,
            major=self.major1,
            accepted=True,
            scholarship=1000,
            enroll_year=2018,
            description="""
                            Some very very good description"""
        )

        self.assertEqual(ap.main_admission().id, admission4.id)
