from django.http import Http404
from rest_framework.response import Response

from sNeeds.base.api.viewsets import CAPIView
from sNeeds.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from sNeeds.apps.estimation.similarApply.models import AppliedStudentDetailedInfo
from sNeeds.apps.estimation.similarApply.serializers import AppliedStudentDetailedInfoSerializer


class SimilarUniversitiesListView(CAPIView):
    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            return Http404

    def get(self, request, form_id, format=None):
        form = self.get_form_obj(form_id)

        related_forms = AppliedStudentDetailedInfo.objects.none()
        form_majors = form.get_related_majors()

        origin_universities = form.universities.all()
        related_forms |= AppliedStudentDetailedInfo.objects.same_origin_universities(origin_universities)

        try:
            # Want to apply is 1 to 1 with form
            want_to_apply = WantToApply.objects.get(student_detailed_info__id=form.id)
            want_to_apply_universities = want_to_apply.universities.all()
            related_forms |= AppliedStudentDetailedInfo.objects.applied_to_universities(want_to_apply_universities)
        except WantToApply.DoesNotExist:
            pass

        related_forms |= AppliedStudentDetailedInfo.objects.same_previous_major(form_majors)
        related_forms |= AppliedStudentDetailedInfo.objects.same_applied_to_major(form_majors)

        related_forms = related_forms.distinct()

        data = AppliedStudentDetailedInfoSerializer(
            related_forms,
            context={'request': request},
            many=True
        ).data

        return Response(data)
