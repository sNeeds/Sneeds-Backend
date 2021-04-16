from django.db.models import Count, Sum
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
        # return ApplyProfile.objects.none()
        form = self.get_form()
        similar_profiles_for_form = SimilarProfilesForForm(form)
        profiles = similar_profiles_for_form.find_similar_profiles()
        # print('count', profiles.aggregate(Count('educations')))
        # tagged_profiles = SimilarProfilesTagger.tag_queryset3(profiles, form)
        # print(tagged_profiles.count())
        # print(tagged_profiles.values_list('educations__major__name', flat=True))
        # print(tagged_profiles.filter(educations__major__name='Materials engineering').count())
        # print(tagged_profiles.filter(educations__major__name='Materials science and engineering\n').count())
        # print(tagged_profiles.filter(educations__major__name='Nanomaterials').count())
        # print(form.last_education().university.name, form.last_education().major.name)
        # print(tagged_profiles.values_list('educations__university__name'))
        # print(tagged_profiles.filter(exact_home_university=True, educations__major__name='Nanomaterials').count())
        # print(tagged_profiles.filter(exact_home_university=True, exact_home_major=True).count())

        # for field in SimilarProfilesTagger.tags_field_title.keys():
        #     s = field
        #     print(s, True, tagged_profiles.filter(**{s: True}).count())
        #     print(s, False, tagged_profiles.filter(**{s: False}).count())
        # s = 'similar_gpa'
        # print(s, True, tagged_profiles.filter(**{s: True}).count())
        # print(s, False, tagged_profiles.filter(**{s: False}).count())
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
            all_ids = all_ids.union(set(filtering_result['ids']))
            res['filters'].append(filtering_result)

        # print('all_ids', len(all_ids))

        queryset = ApplyProfile.objects.prefetch_related('educations', 'publications', 'language_certificates')\
            .filter(id__in=all_ids)

        tagged_queryset = SimilarProfilesTagger.tag_queryset3(queryset, sdi)
        # for a in tagged_queryset:
        #     print(str(a.educations.first().major).strip())
        #     print(str(a.admissions.first().major).strip(), '\n', '----------------------------------------------------')

        res['objects'] = self.get_serializer(tagged_queryset, many=True).data

        # res['objects'] = self.get_serializer(
        #     ApplyProfile.objects.filter(id__in=all_ids)[:7],
        #     many=True).data

        return Response(res)
