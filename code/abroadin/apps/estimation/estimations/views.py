from django.http import Http404
from rest_framework.response import Response

from abroadin.base.api.viewsets import CAPIView

from abroadin.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from abroadin.apps.estimation.estimations.reviews import StudentDetailedFormReview
from abroadin.apps.estimation.estimations.serializers import WantToApplyChanceSerializer


class FormComments(CAPIView):
    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get(self, request, form_id, format=None):
        form = self.get_form_obj(form_id)
        review = StudentDetailedFormReview(form)
        return Response(review.review_all())


class AdmissionRankingChance(CAPIView):
    def get(self, request, form_id, format=None):
        return Response(
            {
                "0-20": {
                    "admission": 0.4,
                    "scholarship": 0,
                    "full-fund": 0
                },
                "20-100": {
                    "admission": 0.8,
                    "scholarship": 0.5,
                    "full-fund": 0.3
                },
                "100-400": {
                    "admission": 1,
                    "scholarship": 0.95,
                    "full-fund": 0.9
                },
                "+400": {
                    "admission": 1,
                    "scholarship": 1,
                    "full-fund": 1
                },
            }
        )


class WantToApplyChance(CAPIView):
    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get(self, request, form_id, format=None):
        form = self.get_form_obj(form_id)
        try:
            want_to_apply = WantToApply.objects.get(student_detailed_info=form)
            want_to_apply_chance_serializer = WantToApplyChanceSerializer(want_to_apply)
            return Response(want_to_apply_chance_serializer.data)

        except WantToApply.DoesNotExist:
            return Response({})
