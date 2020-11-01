from django.http import Http404
from rest_framework.response import Response

from abroadin.base.api.viewsets import CAPIView
from abroadin.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from abroadin.apps.estimation.similarApply.models import AppliedStudentDetailedInfo, AppliedTo
from abroadin.apps.estimation.similarApply.serializers import AppliedToExtendedSerializer


class SimilarUniversitiesListView(CAPIView):
    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            return Http404

    def get(self, request, form_id, format=None):
        form = self.get_form_obj(form_id)

        related_applied_tos = AppliedTo.objects.none()

        try:
            # Want to apply is 1 to 1 with form
            want_to_apply = WantToApply.objects.get(student_detailed_info__id=form.id)

            want_to_apply_universities_list = want_to_apply.universities.all().list()
            related_applied_tos |= AppliedTo.objects.filter(university__in=want_to_apply_universities_list)

            want_to_apply_countries_list = want_to_apply.countries.all().list()
            related_applied_tos |= AppliedTo.objects.filter(university__country__in=want_to_apply_countries_list)

        except WantToApply.DoesNotExist:
            pass

        related_applied_tos = related_applied_tos.distinct()

        data = AppliedToExtendedSerializer(
            related_applied_tos,
            context={'request': request},
            many=True
        ).data

        return Response(data)
