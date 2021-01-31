from abroadin.apps.data.account.models import Country
from abroadin.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from abroadin.apps.applyprofile.models import Admission, ApplyProfile

from ..base import SimilarProfilesBaseTests
from ...functions import get_preferred_apply_country, get_want_to_apply_similar_countries, filter_around_gpa, \
    filter_same_want_to_apply_grades


class SimilarProfilesFunctionsBaseTests(SimilarProfilesBaseTests):
    def setUp(self):
        super().setUp()

        self.canada, _ = Country.objects.get_or_create(name="Canada", search_name="canada", slug="canada")

    def test_get_preferred_apply_country(self):
        self.assertEqual(get_preferred_apply_country(), self.canada)

    def test_get_want_to_apply_similar_countries(self):
        def no_country_no_university_scenario(result):
            self.assertEqual(
                result,
                [get_preferred_apply_country()]
            )

        def country_not_university_one_country_scenario(result):
            self.assertEqual(
                result,
                [self.country1]
            )

        def country_not_university_multiple_country_scenario(result):
            self.assertEqual(
                result,
                [self.country1, self.country2]
            )

        def not_country_university_one_university_scenario(result):
            self.assertEqual(
                result,
                [self.university1.country]
            )

        def not_country_university_multiple_university_scenario(result):
            self.assertEqual(
                result,
                [self.university1.country, self.university2.country]
            )

        def country_university_scenario(result):
            self.assertListEqual(
                result,
                [self.university1.country, self.country2]
            )

        form = StudentDetailedInfo.objects.create(
            user=self.user3,
            age=20,
            gender=StudentDetailedInfo.GenderChoices.MALE,
            related_work_experience=0,
            academic_break=0,
            powerful_recommendation=False
        )

        tested_func = get_want_to_apply_similar_countries

        want_to_apply = WantToApply.objects.create(student_detailed_info=form)
        result = tested_func(want_to_apply)
        no_country_no_university_scenario(result)

        want_to_apply.countries.add(self.country1)
        result = tested_func(want_to_apply)
        country_not_university_one_country_scenario(result)

        want_to_apply.countries.add(self.country2)
        result = tested_func(want_to_apply)
        country_not_university_multiple_country_scenario(result)

        want_to_apply.countries.clear()
        want_to_apply.universities.add(self.university1)
        result = tested_func(want_to_apply)
        not_country_university_one_university_scenario(result)

        want_to_apply.universities.add(self.university2)
        result = tested_func(want_to_apply)
        not_country_university_multiple_university_scenario(result)

        want_to_apply.universities.add(self.university1)
        assert self.university1.country != self.country2
        want_to_apply.countries.add(self.country2)
        country_university_scenario(result)

    def test_filter_around_gpa(self):
        func = filter_around_gpa

    def test_filter_same_want_to_apply_grades(self):
        func = filter_same_want_to_apply_grades

        Admission.objects.create(
            apply_profile=self.profile_1,
            major=self.major1,
            grade=self.grade1,
            destination=self.university1,
            accepted=True,
            scholarship=25000,
            enroll_year=2020
        )

        Admission.objects.create(
            apply_profile=self.profile_2,
            major=self.major1,
            grade=self.grade2,
            destination=self.university1,
            accepted=True,
            scholarship=25000,
            enroll_year=2020
        )

        profiles = ApplyProfile.objects.filter(id=self.profile_1.id)
        result = func(profiles, [self.grade1])
        self.assertQuerysetEqual(result, profiles, transform=lambda x: x)

        profiles = ApplyProfile.objects.filter(id=self.profile_2.id)
        result = func(profiles, [self.grade2])
        self.assertQuerysetEqual(result, profiles, transform=lambda x: x)

        profiles = ApplyProfile.objects.filter(id__in=[self.profile_1.id, self.profile_2.id])
        result = func(profiles, [self.grade1, self.grade2])
        self.assertQuerysetEqual(result, profiles, transform=lambda x: x, ordered=False)

        profiles = ApplyProfile.objects.none()
        result = func(profiles, [self.grade1, self.grade2])
        self.assertQuerysetEqual(result, profiles, transform=lambda x: x)

        profiles = ApplyProfile.objects.filter(id__in=[self.profile_1.id, self.profile_2.id])
        result = func(profiles, [self.grade3])
        self.assertQuerysetEqual(result, ApplyProfile.objects.none(), transform=lambda x: x)
