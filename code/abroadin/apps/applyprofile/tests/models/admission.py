from .base import ApplyProfileModelsTestBase
from ...models import ApplyProfile, Admission


class AdmissionModelTests(ApplyProfileModelsTestBase):

    def setUp(self) -> None:
        super(ApplyProfileModelsTestBase, self).setUp()

        self.apply_profile1 = ApplyProfile.objects.create(
            name='apply profile 1',
            gap=6,
        )

    def test_admission_creation_correct(self):
        admission = Admission.objects.create(
            apply_profile=self.apply_profile1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=True,
            scholarship=1000,
            enroll_year=2018,
            description="""
            Some very very good description"""
        )

        self.assertEqual(admission.apply_profile, self.apply_profile1)
        self.assertEqual(admission.major, self.major1)
        self.assertEqual(admission.grade, self.bachelor_grade)
        self.assertEqual(admission.destination, self.university1)
        self.assertEqual(admission.accepted, True)
        self.assertEqual(admission.scholarship, 1000)
        self.assertEqual(admission.enroll_year, 2018)
        self.assertIsNotNone(admission.description)

    def test_two_admission_for_apply_profile(self):
        admission1 = Admission.objects.create(
            apply_profile=self.apply_profile1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=True,
            scholarship=1000,
            enroll_year=2018,
            description="""
                    Some very very good description"""
        )

        admission2 = Admission.objects.create(
            apply_profile=self.apply_profile1,
            major=self.major1,
            grade=self.master_grade,
            destination=self.university2,
            accepted=True,
            scholarship=1500,
            enroll_year=2018,
            description="""
                    Some very very good description"""
        )

        self.assertEqual(self.apply_profile1.admissions.count(), 2)

    def test_order_by_grade_query(self):
        admission1 = Admission.objects.create(
            apply_profile=self.apply_profile1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=True,
            scholarship=1000,
            enroll_year=2018,
            description="""
                    Some very very good description"""
        )

        admission2 = Admission.objects.create(
            apply_profile=self.apply_profile1,
            major=self.major1,
            grade=self.master_grade,
            destination=self.university2,
            accepted=True,
            scholarship=1500,
            enroll_year=2018,
            description="""
                    Some very very good description"""
        )

        admission3 = Admission.objects.create(
            apply_profile=self.apply_profile1,
            major=self.major1,
            grade=self.phd_grade,
            destination=self.university2,
            accepted=True,
            scholarship=1500,
            enroll_year=2018,
            description="""
                    Some very very good description"""
        )

        self.assertEqual(self.apply_profile1.admissions.order_by_grade().first().id, admission1.id)
