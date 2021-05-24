from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from abroadin.base.api.generics import CListAPIView
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer

from abroadin.apps.estimation.form.permissions import IsFormOwner, CompletedForm
from abroadin.apps.users.customAuth.permissions import UserEmailIsVerified

from .functions import SimilarProfilesForForm
from .pipeline import SimilarProfilesPipelineObject
from .taggers import SimilarProfilesTagger
from ...applyprofile.models import ApplyProfile


class ProfilesListAPIView(CListAPIView):
    lookup_url_kwarg = 'form_id'
    serializer_class = ApplyProfileSerializer
    permission_classes = [IsAuthenticated,
                          IsFormOwner,
                          CompletedForm,
                          UserEmailIsVerified
                          ]

    def get_form(self):
        form_id = self.kwargs[self.lookup_url_kwarg]
        try:
            return StudentDetailedInfo.objects.prefetch_related('educations') \
                .select_related('want_to_apply').get(id=form_id)
            # return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get_queryset(self):
        form = self.get_form()
        similar_profiles_for_form = SimilarProfilesForForm(form)
        profiles = similar_profiles_for_form.find_similar_profiles()
        return profiles[:7]


class ProfilesListAPIViewVersion2(ProfilesListAPIView):
    serializer_class = ApplyProfileSerializer
    queryset = ApplyProfile.objects.all()

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        sdi = self.get_form()

        filtering_results = SimilarProfilesPipelineObject.get_filter_results(queryset, sdi)
        res = {}
        res['filters'] = []
        all_ids = set()

        for filtering_result in filtering_results:
            #if len(filtering_result['ids']) == 0:
            #    continue
            all_ids = all_ids.union(set(filtering_result['ids']))
            del(filtering_result['qs'])
            res['filters'].append(filtering_result)

        queryset = ApplyProfile.objects.prefetch_related('educations', 'publications', 'language_certificates')\
            .filter(id__in=all_ids)

        tagged_queryset = SimilarProfilesTagger.tag_queryset3(queryset, sdi)

        res_objects = self.get_serializer(tagged_queryset, many=True).data

        def refine_tags(tags):
            refined_tags = []
            for tag in tags:
                if tag.startswith('Similar') and tag.replace('Similar', 'Exact') in tags:
                    continue
                refined_tags.append(tag)
            return refined_tags

        for obj in res_objects:
            obj['tags'] = refine_tags(obj['tags'])

        res['objects'] = res_objects

        return Response(res)
