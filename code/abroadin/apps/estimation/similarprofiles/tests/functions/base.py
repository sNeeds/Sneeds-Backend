from django.contrib.contenttypes.models import ContentType

from abroadin.apps.data.account.models import Country
from abroadin.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from abroadin.apps.applyprofile.models import Admission, ApplyProfile
from abroadin.apps.data.applydata.models import Education, GradeChoices

from ..base import SimilarProfilesTestsBase
from ...functions import get_preferred_apply_country, get_want_to_apply_similar_countries, filter_around_gpa, \
    filter_same_want_to_apply_grades, similar_destination_Q, filter_similar_majors, filter_similar_home_and_destination


class SimilarProfilesFunctionsBaseTests(SimilarProfilesTestsBase):
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

        content_type = ContentType.objects.get(app_label='applyprofile', model='applyprofile')
        Education.objects.create(
            content_type=content_type,
            object_id=self.profile_1.id,
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major1,
            graduate_in=2020,
            gpa=16
        )

        Education.objects.create(
            content_type=content_type,
            object_id=self.profile_2.id,
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major1,
            graduate_in=2020,
            gpa=20
        )

        profiles_qs = ApplyProfile.objects.filter(id__in=[self.profile_1.id, self.profile_2.id])
        filtered_profiles_qs = func(profiles_qs, 15, 2)
        self.assertQuerysetEqual(ApplyProfile.objects.filter(id=self.profile_1.id), filtered_profiles_qs, lambda x: x)

        filtered_profiles_qs = func(profiles_qs, 17, 2)
        self.assertQuerysetEqual(ApplyProfile.objects.filter(id=self.profile_1.id), filtered_profiles_qs, lambda x: x)

        filtered_profiles_qs = func(profiles_qs, 17, 3)
        self.assertQuerysetEqual(profiles_qs, filtered_profiles_qs, lambda x: x, ordered=False)

        filtered_profiles_qs = func(profiles_qs, 5, 1)
        self.assertQuerysetEqual(ApplyProfile.objects.none(), filtered_profiles_qs, lambda x: x)

    def test_filter_same_want_to_apply_grades(self):
        func = filter_same_want_to_apply_grades

        Admission.objects.create(
            apply_profile=self.profile_1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=True,
            scholarship=25000,
            enroll_year=2020
        )

        Admission.objects.create(
            apply_profile=self.profile_2,
            major=self.major1,
            grade=self.master_grade,
            destination=self.university1,
            accepted=True,
            scholarship=25000,
            enroll_year=2020
        )

        profiles = ApplyProfile.objects.filter(id=self.profile_1.id)
        result = func(profiles, [self.bachelor_grade])
        self.assertQuerysetEqual(result, profiles, transform=lambda x: x)

        profiles = ApplyProfile.objects.filter(id=self.profile_2.id)
        result = func(profiles, [self.master_grade])
        self.assertQuerysetEqual(result, profiles, transform=lambda x: x)

        profiles = ApplyProfile.objects.filter(id__in=[self.profile_1.id, self.profile_2.id])
        result = func(profiles, [self.bachelor_grade, self.master_grade])
        self.assertQuerysetEqual(result, profiles, transform=lambda x: x, ordered=False)

        profiles = ApplyProfile.objects.none()
        result = func(profiles, [self.bachelor_grade, self.master_grade])
        self.assertQuerysetEqual(result, profiles, transform=lambda x: x)

        profiles = ApplyProfile.objects.filter(id__in=[self.profile_1.id, self.profile_2.id])
        result = func(profiles, [self.phd_grade])
        self.assertQuerysetEqual(result, ApplyProfile.objects.none(), transform=lambda x: x)

    def test_similar_home_Q(self):
        raise NotImplementedError

    def test_similar_destination_Q(self):
        func = similar_destination_Q

        Admission.objects.create(
            apply_profile=self.profile_1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=True,
            scholarship=25000,
            enroll_year=2020
        )

        Admission.objects.create(
            apply_profile=self.profile_2,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university2,
            accepted=True,
            scholarship=25000,
            enroll_year=2020
        )

        profiles = ApplyProfile.objects.filter(id__in=[self.profile_1.id, self.profile_2.id])

        countries = Country.objects.filter(id=self.university1.country.id)
        q = func(countries)
        filtered_profiles_qs = profiles.filter(q)
        self.assertQuerysetEqual(
            filtered_profiles_qs, ApplyProfile.objects.filter(id=self.profile_1.id),
            transform=lambda x: x, ordered=False
        )

        countries = Country.objects.filter(id__in=[self.university1.id, self.university2.id])
        q = func(countries)
        filtered_profiles_qs = profiles.filter(q)
        self.assertQuerysetEqual(
            filtered_profiles_qs, ApplyProfile.objects.filter(id__in=[self.profile_1.id, self.profile_2.id]),
            transform=lambda x: x, ordered=False
        )

        countries = Country.objects.none()
        q = func(countries)
        filtered_profiles_qs = profiles.filter(q)
        self.assertQuerysetEqual(
            filtered_profiles_qs, ApplyProfile.objects.none(),
            transform=lambda x: x, ordered=False
        )

    def test_filter_similar_home_and_destination(self):
        func = filter_similar_home_and_destination
        raise NotImplemented

    def test_filter_similar_majors(self):
        def test_qs_equal(profiles, filtered_profiles, majors):
            qs = func(profiles, majors)
            self.assertQuerysetEqual(qs, filtered_profiles, lambda x: x, ordered=False)

        func = filter_similar_majors
        profiles = ApplyProfile.objects.filter(id=self.profile_1.id)

        test_qs_equal(profiles, profiles.none(), [])
        test_qs_equal(profiles, profiles.none(), [self.major1])
        test_qs_equal(profiles, profiles.none(), [self.major1, self.major2])

        content_type = ContentType.objects.get(app_label='applyprofile', model='applyprofile')
        education = Education.objects.create(
            content_type=content_type,
            object_id=self.profile_1.id,
            university=self.university1,
            grade=self.bachelor_grade,
            major=self.major1,
            graduate_in=2020,
            gpa=16
        )
        test_qs_equal(profiles, profiles, [self.major1])
        test_qs_equal(profiles, profiles.none(), [self.major2])
        education.delete()

        admission = Admission.objects.create(
            apply_profile=self.profile_1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=True,
            scholarship=25000,
            enroll_year=2020
        )
        test_qs_equal(profiles, profiles.none(), [self.major2])
        test_qs_equal(profiles, profiles, [self.major1])
        admission.delete()

        education = Education.objects.create(
            content_type=content_type,
            object_id=self.profile_1.id,
            university=self.university1,
            grade=self.bachelor_grade,
            major=self.major1,
            graduate_in=2020,
            gpa=16
        )
        admission = Admission.objects.create(
            apply_profile=self.profile_1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=True,
            scholarship=25000,
            enroll_year=2020
        )
        test_qs_equal(profiles, profiles, [self.major1])
        test_qs_equal(profiles, profiles.none(), [self.major2])

        Education.objects.create(
            content_type=content_type,
            object_id=self.profile_2.id,
            university=self.university1,
            grade=self.bachelor_grade,
            major=self.major2,
            graduate_in=2020,
            gpa=16
        )
        profiles = ApplyProfile.objects.filter(id__in=[self.profile_1.id, self.profile_2.id])
        test_qs_equal(profiles, profiles.filter(id=self.profile_1.id), [self.major1])
