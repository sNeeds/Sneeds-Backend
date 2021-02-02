from django.http import Http404

from abroadin.base.api.generics import CListAPIView
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer

from .functions import  SimilarProfilesForForm


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
        return profiles[:7]
