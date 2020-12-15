from django.shortcuts import render
from rest_framework.response import Response

from abroadin.apps.testapps.similarProfiles.profiles import Profile
from abroadin.apps.data.account.models import University, Major
from abroadin.apps.estimation.form.models import GradeChoices, StudentDetailedInfo
from base.api.viewsets import CAPIView


class SimilarProfiles(CAPIView):
    form = None

    def set_form(self, form_id):
        self.form = StudentDetailedInfo.objects.get(id=form_id)

    def get_form(self):
        return self.form

    def _create_profile_1(self):
        profile = Profile()

        profile.match_percent = "91"
        profile.language_certificate = "IELTS 7"
        profile.home_university = University.objects.get("McGill University")
        profile.home_major = Major.objects.get("Computer science")

        profile.accepted_universities_number = 4
        profile.destination_university = University.objects.get("McGill University")
        profile.destination_major = Major.objects.get("Computer science")
        profile.destination_grade = GradeChoices.PHD
        profile.destination_scholarship = "Full Fund (21000$/Y)"

        profile.rejected_universities_number = 3
        profile.destination_rejected_university = University.objects.get("University of Oxford")
        profile.destination_rejected_year = 2019
        profile.destination_rejected_major = Major.objects.get("Computer science")
        profile.destination_rejected_scholarship = "No fund granted"

        return profile

    def get(self, form_id, *args, **kwargs):
        self.set_form(form_id)

        profile_1 = self._create_profile_1()
        profile_2 = self._create_profile_1()

        data = {
            [
                profile_1.get_json(),
                profile_2.get_json()
            ]
        }

        return Response(data)
