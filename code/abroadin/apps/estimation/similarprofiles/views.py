from django.http import Http404

from abroadin.base.api.generics import CListAPIView
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer

from .functions import SimilarProfilesForForm
from .taggers import SimilarProfilesTagger


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
        similar_profiles_for_form = SimilarProfilesForForm(form)
        profiles = similar_profiles_for_form.find_similar_profiles()
        tagged_profiles = SimilarProfilesTagger.tag_queryset(profiles, form)
        print(tagged_profiles.count())
        # print(tagged_profiles.values_list('educations__major__name', flat=True))
        # print(tagged_profiles.filter(educations__major__name='Materials engineering').count())
        # print(tagged_profiles.filter(educations__major__name='Materials science and engineering\n').count())
        # print(tagged_profiles.filter(educations__major__name='Nanomaterials').count())
        print(form.last_education().university.name, form.last_education().major.name)
        # print(tagged_profiles.values_list('educations__university__name'))
        print(tagged_profiles.filter(exact_home_university=True, educations__major__name='Nanomaterials').count())
        print(tagged_profiles.filter(exact_home_university=True, exact_home_major=True).count())
        print('aaa', tagged_profiles.filter(aaa=False).count())
        print('aaa', tagged_profiles.filter(aaa=True).count())
        return tagged_profiles[:7]
