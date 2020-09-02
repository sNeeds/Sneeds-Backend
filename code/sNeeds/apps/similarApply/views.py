from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView

from sNeeds.apps.account.models import StudentDetailedInfo
from sNeeds.apps.similarApply.models import AppliedStudentDetailedInfo


class SimilarUniversitiesListView(APIView):
    def get_form_object(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get(self, request, form_id, format=None):
        form = self.get_form_object(form_id)

        # Want to apply is 1 to 1 with form
        want_to_apply = form.want_to_apply.all().first()
        universities = want_to_apply.universities.all()

        related_forms = AppliedStudentDetailedInfo.objects.none()

        related_forms |= AppliedStudentDetailedInfo.objects.get_applied_to_universities(universities)
        related_forms |= AppliedStudentDetailedInfo.objects.get_applied_to_universities(universities)
        related_forms |= AppliedStudentDetailedInfo.objects.get_applied_to_universities(universities)
