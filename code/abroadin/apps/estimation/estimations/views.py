from django.http import Http404
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from abroadin.apps.estimation.form.permissions import CompletedForm, IsFormOwner
from abroadin.base.api.viewsets import CAPIView

from abroadin.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from abroadin.apps.estimation.estimations.reviews import StudentDetailedFormReview
from abroadin.apps.estimation.estimations.chances import AdmissionChance

from .admission_chance_test_tool import AdmissionChanceResultTest
from ...users.customAuth.permissions import IsStaff


class FormComments(CAPIView):
    lookup_url_kwarg = 'form_id'
    permission_classes = [CompletedForm, IsFormOwner]

    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get(self, request, form_id, format=None):
        self.kwargs[self.lookup_url_kwarg] = form_id

        form = self.get_form_obj(form_id)
        review = StudentDetailedFormReview(form)
        return Response(review.review_all())


class AdmissionRankingChance(CAPIView):
    lookup_url_kwarg = 'form_id'
    permission_classes = [CompletedForm, IsFormOwner]

    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get(self, request, form_id, format=None):
        self.kwargs[self.lookup_url_kwarg] = form_id
        form = self.get_form_obj(form_id)
        admission_chance = AdmissionChance(form)

        data = {
            "0-20": admission_chance.get_1_to_20_chance(),
            "20-100": admission_chance.get_21_to_100_chance(),
            "100-400": admission_chance.get_101_to_400_chance(),
            "+400": admission_chance.get_401_above_chance(),
        }

        return Response(data)


class WantToApplyChance(CAPIView):
    lookup_url_kwarg = 'form_id'
    permission_classes = [CompletedForm, IsFormOwner]

    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get(self, request, form_id, format=None):
        self.kwargs[self.lookup_url_kwarg] = form_id

        data = []
        form = self.get_form_obj(form_id)

        try:
            admission_chance = AdmissionChance(form)
            want_to_apply = WantToApply.objects.get(student_detailed_info__id=form.id)

            for university in want_to_apply.universities.all().order_by('rank'):
                values_and_labels = {}
                values_and_labels["university"] = university.name
                values_and_labels["rank"] = university.rank
                values_and_labels["chances"] = admission_chance.get_university_chance_with_label(university)
                data.append(values_and_labels)

            return Response(data)

        except WantToApply.DoesNotExist:
            return Response({})


class AdmissionChanceTestAPIView(CAPIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def get(self, request):
        admission_chance_result_test = AdmissionChanceResultTest()
        admission_chance_result_test.test_results()
        return Response({'failures': admission_chance_result_test.failures})
