from django.db.models import Q
from django.http import Http404

from abroadin.base.api.generics import CListAPIView
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer
from abroadin.apps.data.account.models import Major, Country
from abroadin.apps.applyprofile.models import ApplyProfile

from .functions import get_want_to_apply_similar_countries,\
    filter_same_want_to_apply_grades, filter_similar_majors, \
    filter_similar_home_and_destination


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

        want_to_apply = form.get_want_to_apply_or_none()
        education_qs = form.education_qs()

        education_major_ids = education_qs.get_majors_id_list()
        education_majors_qs = Major.objects.id_to_qs(education_major_ids)

        want_to_apply_majors_qs = want_to_apply.majors.all()

        form_related_majors = education_majors_qs | want_to_apply_majors_qs
        form_related_majors_parents = form_related_majors.top_nth_parents(3)
        form_related_majors_all_children = form_related_majors_parents.get_all_children_majors()

        grades_want_to_apply = want_to_apply.grades_want_to_apply()
        similar_destination_countries = get_want_to_apply_similar_countries(want_to_apply)

        profiles = ApplyProfile.objects.all()
        profiles = filter_same_want_to_apply_grades(profiles, grades_want_to_apply)
        profiles = filter_similar_majors(profiles, form_related_majors_all_children)
        profiles = filter_similar_home_and_destination(profiles, similar_destination_countries)

        return profiles[:7]
