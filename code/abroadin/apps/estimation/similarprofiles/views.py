from django.db.models import Q
from django.http import Http404

from abroadin.base.api.generics import CListAPIView
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer
from abroadin.apps.data.account.models import Major
from abroadin.apps.applyprofile.models import ApplyProfile


class ProfilesListAPIView(CListAPIView):
    lookup_url_kwarg = 'form_id'
    serializer_class = ApplyProfileSerializer

    def get_form(self):
        form_id = self.kwargs[self.lookup_url_kwarg]
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def _filter_same_want_to_apply_grades(self, profiles, grades):
        profiles_qs = profiles.filter(admission__grade__in=grades)
        return profiles_qs

    # def _filter_similar_majors(self, majors):

    def get_queryset(self):
        form = self.get_form()

        want_to_apply = form.get_want_to_apply_or_none()
        education_qs = form.education_qs()

        education_major_ids = education_qs.get_majors_id_list()
        education_majors_qs = Major.objects.id_to_qs(education_major_ids)

        want_to_apply_majors_qs = want_to_apply.majors.all()

        form_related_majors = education_majors_qs | want_to_apply_majors_qs
        form_related_majors_parents = form_related_majors.top_nth_parents(3)

        grades_want_to_apply = want_to_apply.grades_want_to_apply()

        profiles = ApplyProfile.objects.all()
        profiles = self._filter_same_want_to_apply_grades(profiles, grades_want_to_apply)
        # print(profiles)

        major1 = Major.objects.all()[1]
        print(major1)
        print(major1.get_all_children_majors())
        return profiles
