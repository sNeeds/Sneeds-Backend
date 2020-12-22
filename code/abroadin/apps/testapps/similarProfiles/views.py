from django.shortcuts import render
from rest_framework.response import Response

from abroadin.base.api.viewsets import CAPIView
from abroadin.apps.testapps.similarProfiles.profiles import Profile
from abroadin.apps.data.account.models import University, Major, Country
from abroadin.apps.estimation.form.models import GradeChoices, StudentDetailedInfo
from abroadin.apps.estimation.estimations.chances import AdmissionChance
from abroadin.apps.data.account.serializers import UniversitySerializer


class SimilarProfiles(CAPIView):
    form = None

    def set_form(self, form_id):
        self.form = StudentDetailedInfo.objects.get(id=form_id)

    def get_form(self):
        return self.form

    def destination_university(self):
        def _acceptable_university(universities, admission_chance):
            ACCEPTED_ADMISSION_CHANCE_VALUE = 0.5

            for university in universities:
                admission_chance_value = admission_chance.get_university_chance(university)["admission"]
                if ACCEPTED_ADMISSION_CHANCE_VALUE < admission_chance_value:
                    return university

            return None

        def _preferred_country_or_none(countries):
            canada = Country.objects.get(name="Canada")
            usa = Country.objects.get(name="United States")

            if canada in countries:
                return canada
            elif usa in countries:
                return usa

            return None

        picked_universities = {
            "usa": [
                University.objects.get(name="Princeton University"),  # 12
                University.objects.get(name="University of Washington"),  # 73
                University.objects.get(name="University of Virginia"),  # 219
                University.objects.get(name="Colorado State University"),  # 443
            ],
            "canada": [
                University.objects.get(name="McGill University"),  # 33
                University.objects.get(name="University of Alberta"),  # 120
                University.objects.get(name="Université Laval"),  # 420
            ],
            "europe": [
                University.objects.get(name="École Polytechnique Fédérale de Lausanne (EPFL)"),  # 14,
                University.objects.get(name="The University of Melbourne"),  # 41,
                University.objects.get(name="Politecnico di Milano"),  # 137,
                University.objects.get(name="University of Trento"),  # 406,
            ]
        }

        form = self.form
        admission_chance = AdmissionChance(form)
        want_to_apply = form.get_want_to_apply_or_none()

        if not want_to_apply.universities.all().exists():
            countries = want_to_apply.countries.all()
            preferred_country = _preferred_country_or_none(countries)

            if not countries.exists():
                universities = picked_universities["canada"]
            elif preferred_country == Country.objects.get(name="United States"):
                universities = picked_universities["usa"]
            elif preferred_country == Country.objects.get(name="Canada"):
                universities = picked_universities["canada"]
            else:
                universities = picked_universities["europe"]

            university = _acceptable_university(universities, admission_chance)

        else:
            universities = want_to_apply.universities.all().order_by('-rank')
            university = _acceptable_university(universities, admission_chance)
            if university is None:
                university = _acceptable_university(picked_universities["canada"], admission_chance)
                if university is None:
                    university = picked_universities["canada"][-1]

        return university

    def near_university(self, university, ranks_above):
        return University.objects.filter(
            country=university.country,
            rank__gte=university.rank
        ).order_by('rank')[ranks_above]

    def _create_profile_1(self):
        profile = Profile()
        form = self.get_form()
        last_university_through = form.last_university_through()

        profile.match_percent = "91%"
        profile.language_certificate = "7.5 Overall"
        profile.home_university = last_university_through.university
        if last_university_through.major.parent_major:
            profile.home_major = last_university_through.major.parent_major
        else:
            profile.home_major = last_university_through.major

        profile.accepted_universities_number = 4
        profile.destination_university = self.destination_university()
        profile.destination_major = last_university_through.major
        profile.destination_grade = GradeChoices.higher_grade_or_same(last_university_through.grade)
        profile.destination_scholarship = "Full Fund - 21000$/Y"

        profile.rejected_universities_number = 3
        profile.destination_rejected_university = self.near_university(profile.destination_university, 1)
        profile.destination_rejected_year = "Winter 2019"
        if last_university_through.major.parent_major:
            profile.destination_rejected_major = last_university_through.major.parent_major
        else:
            profile.destination_rejected_major = last_university_through.major
        profile.destination_rejected_scholarship = "No fund granted"

        return profile

    def _create_profile_2(self):
        profile = Profile()
        form = self.get_form()
        last_university_through = form.last_university_through()

        profile.match_percent = "85%"
        profile.language_certificate = "7 Overall"
        profile.home_university = last_university_through.university
        profile.home_major = last_university_through.major

        profile.accepted_universities_number = 2
        profile.destination_university = self.near_university(self.destination_university(), 2)
        profile.destination_major = last_university_through.major
        profile.destination_grade = GradeChoices.higher_grade_or_same(last_university_through.grade)
        profile.destination_scholarship = "Full Fund - 25000$/Y"

        profile.rejected_universities_number = 5
        profile.destination_rejected_university = self.near_university(profile.destination_university, 1)
        profile.destination_rejected_year = "Fall 2020"
        profile.destination_rejected_major = last_university_through.major
        profile.destination_rejected_scholarship = "No fund granted"

        return profile

    def get(self, request, form_id, format=None):
        self.set_form(form_id)

        profile_1 = self._create_profile_1()
        profile_2 = self._create_profile_2()

        data = {
            "profiles": [
                profile_1.get_json(),
                profile_2.get_json()
            ]
        }

        return Response(data)
