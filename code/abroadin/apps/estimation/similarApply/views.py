import decimal

from django.http import Http404
from rest_framework.response import Response

from abroadin.base.api.viewsets import CAPIView
from abroadin.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from abroadin.apps.estimation.similarApply.models import AppliedStudentDetailedInfo, AppliedTo
from abroadin.apps.estimation.similarApply.serializers import AppliedToExtendedSerializer
from abroadin.apps.data.account.serializers import UniversitySerializer
from apps.data.account.models import University
from apps.estimation.estimations.chances import AdmissionChance


class SimilarUniversitiesListView(CAPIView):
    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            return Http404

    def get_home_university(self, form):
        last_university_through = form.get_last_university_through()
        return last_university_through.university.name if last_university_through is not None else None

    def get_home_university_gpa(self, form):
        last_university_through = form.get_last_university_through()
        return last_university_through.gpa if last_university_through is not None else None

    def get_major(self, form):
        last_university_through = form.get_last_university_through()
        return last_university_through.major.name if last_university_through is not None else None

    def get_gpa(self, form):
        last_university_through = form.get_last_university_through()
        gpa = last_university_through.gpa if last_university_through is not None else None

        if gpa:
            margin = (form.id.int % 30 - 15) / 10
            margin = min(margin, 1)
            margin = max(margin, -1)
            gpa += decimal.Decimal(margin)
            gpa = min(gpa, 20)
            gpa = max(0, gpa)

        return gpa

    def get_applied_university_data(self, form):
        UNI_UNDER_20 = University.objects.get(name="Princeton University")
        UNI_21_100 = University.objects.get(name="Princeton University")
        UNI_101_400 = University.objects.get(name="Princeton University")
        UNI_ABOVE_400 = University.objects.get(name="Princeton University")

        ACCEPTED_ADMISSION_CHANCE = 0.4

        def generate_applied_university(admission_chance):
            for university in {UNI_UNDER_20, UNI_21_100, UNI_101_400, UNI_ABOVE_400}:
                
                if ACCEPTED_ADMISSION_CHANCE admission_chance.get_university_chance()
                return university
            if admission_chance.university_chance(UNI_UNDER_20) > ACCEPTED_ADMISSION_CHANCE:
                return UNI_UNDER_20
            elif admission_chance.university_chance(UNI_21_100) > ACCEPTED_ADMISSION_CHANCE:
                return UNI

        admission_chance = AdmissionChance(form)
        data = {
            "top_20": admission_chance.get_1_to_20_chance(),
            "20-100": admission_chance.get_21_to_100_chance(),
            "100-400": admission_chance.get_101_to_400_chance(),
            "+400": admission_chance.get_401_above_chance(),
        }

        want_to_apply = form.get_want_to_apply_or_none()

        if not want_to_apply:
            return None

        want_to_apply_universities = want_to_apply.universities.all()
        if not want_to_apply_universities.exists():
            return None

        return UniversitySerializer(
            want_to_apply_universities[0], context={"request": self.request}
        ).data

    def get(self, request, form_id, format=None):
        form = self.get_form_obj(form_id)

        data = [
            {
                "home_university": self.get_home_university(form),
                "home_university_gpa": self.get_home_university_gpa(form),
                "applied_university": self.get_applied_university_data(form),
                "major": self.get_major(form),
                "grade": form.get_last_university_grade(),
                "gpa": self.get_gpa(form),
                "graduate_year": 2019,
                "language_certificate": "IELTS 7.5 & GRE",
                "fund": "30,000$/year",
                "accepted": True
            }
        ]

        return Response(data)
        # For later use

        # related_applied_tos = AppliedTo.objects.none()
        #
        # try:
        #     # Want to apply is 1 to 1 with form
        #     want_to_apply = WantToApply.objects.get(student_detailed_info__id=form.id)
        #
        #     # Same university destination
        #     want_to_apply_universities_list = want_to_apply.universities.all().list()
        #     related_applied_tos |= AppliedTo.objects.filter(university__in=want_to_apply_universities_list)
        #
        #     # Same country destination
        #     want_to_apply_countries_list = want_to_apply.countries.all().list()
        #     related_applied_tos |= AppliedTo.objects.filter(university__country__in=want_to_apply_countries_list)
        #
        #     # Filter only AppliedTos which specified in want to apply grades
        #     want_to_apply_grades = want_to_apply.grades.all()
        #     if want_to_apply_grades:  # list exists
        #         related_applied_tos = related_applied_tos.filter(
        #             grade__in=want_to_apply_grades.values_list('name', flat=True)
        #         )
        #
        #     related_applied_tos = related_applied_tos.filter(accepted=True)
        #     related_applied_tos = related_applied_tos.distinct()
        #
        # data = AppliedToExtendedSerializer(
        #         related_applied_tos,
        #         context={'request': request},
        #         many=True
        #     ).data
        #
        #     return Response(data)
        #
        # except WantToApply.DoesNotExist:
        #     return Response([])
