import uuid

from django.http import Http404
from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.apps.account.models import StudentDetailedInfo, WantToApply
from sNeeds.apps.similarApply.models import AppliedStudentDetailedInfo
from sNeeds.apps.similarApply.serializers import AppliedStudentDetailedInfoSerializer


class SimilarUniversitiesListView(APIView):
    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            return None

    def get(self, request, form_id, format=None):
        form = self.get_form_obj(form_id)
        related_forms = AppliedStudentDetailedInfo.objects.none()

        origin_universities = form.universities.all()
        related_forms |= AppliedStudentDetailedInfo.objects.same_origin_universities(origin_universities)

        try:
            # Want to apply is 1 to 1 with form
            want_to_apply = WantToApply.objects.get(student_detailed_info__id=form.id)
            want_to_apply_universities = want_to_apply.universities.all()
            related_forms |= AppliedStudentDetailedInfo.objects.applied_to_universities(want_to_apply_universities)
        except WantToApply.DoesNotExist:
            pass

        data = AppliedStudentDetailedInfoSerializer(
            related_forms,
            context={'request': request},
            many=True
        ).data

        print(type(data))
        print(data)

        return Response(data)
