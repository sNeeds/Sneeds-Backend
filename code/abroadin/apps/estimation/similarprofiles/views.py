from django.db.models import Q
from django.http import Http404

from abroadin.base.api.generics import CListAPIView
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer
from abroadin.apps.data.account.models import Major
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

        print(1)
        want_to_apply = form.get_want_to_apply_or_none()
        print(2)
        education_qs = form.education_qs()
        print(3)

        education_major_ids = education_qs.get_majors_id_list()
        print(4)
        education_majors_qs = Major.objects.id_to_qs(education_major_ids)
        print(5)

        want_to_apply_majors_qs = want_to_apply.majors.all()
        print(6)

        form_related_majors = education_majors_qs | want_to_apply_majors_qs
        print(7)
        form_related_majors_parents = form_related_majors.top_nth_parents(3)
        print(8)
        form_related_majors_all_children = form_related_majors_parents.get_all_children_majors()
        print(9)

        grades_want_to_apply = want_to_apply.grades_want_to_apply()
        print(10)
        similar_destination_countries = get_want_to_apply_similar_countries(want_to_apply)
        print(11)

        profiles = ApplyProfile.objects.all()
        print(12)
        profiles = filter_same_want_to_apply_grades(profiles, grades_want_to_apply)
        print(13)
        profiles = filter_similar_majors(profiles, form_related_majors_all_children)
        print(14)
        profiles = filter_similar_home_and_destination(profiles, similar_destination_countries)
        print(15)

        profiles = profiles.distinct()
        print(16)
        return profiles[:7]
