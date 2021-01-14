from django.http import Http404

from abroadin.base.api.generics import CListAPIView
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer
from abroadin.apps.data.account.models import Major


class ProfilesListAPIView(CListAPIView):
    lookup_url_kwarg = 'form_id'
    serializer_class = ApplyProfileSerializer

    def get_form(self):
        form_id = self.kwargs[self.lookup_url_kwarg]
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get_queryset(self):
        form = self.get_form()

        last_grade = form.get_last_university_grade()
        education_qs = form.education_qs()
        major_ids = education_qs.get_majors_id_list()
        majors_qs = Major.objects.id_to_qs(major_ids)
        major_top_three_parents = majors_qs.top_nth_parents(3)

        print(last_grade)
        print(major_top_three_parents)

        print(self.kwargs)
        # return Response({})
