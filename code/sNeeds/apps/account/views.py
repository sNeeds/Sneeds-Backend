from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions

from . import models
from . import serializers
from .models import StudentDetailedInfo, StudentFormApplySemesterYear, BasicFormField
from .permissions import IsStudentPermission,\
    StudentDetailedInfoOwnerOrInteractConsultantOrWithoutUserPermission, \
    IsGMATCertificateOwnerOrDetailedInfoWithoutUser, IsGRECertificateOwnerOrDetailedInfoWithoutUser,\
    IsWantToApplyOwnerOrDetailedInfoWithoutUser, IsPublicationOwnerOrDetailedInfoWithoutUser,\
    IsUniversityThroughOwnerOrDetailedInfoWithoutUser, \
    IsLanguageCertificateTypeThroughOwnerOrDetailedInfoWithoutUser
from .serializers import StudentDetailedInfoSerializer, StudentFormApplySemesterYearSerializer, \
    BasicFormFieldSerializer, StudentDetailedInfoRequestSerializer
from ...utils.custom.views import custom_generic_apiviews


class CountryDetail(generics.RetrieveAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    lookup_field = 'slug'


class CountryList(generics.ListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        from sNeeds.apps.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        country_list = list(study_info_with_active_consultant_qs.values_list('university__country_id', flat=True))
        return models.Country.objects.filter(id__in=country_list).exclude(slug="iran")


class UniversityDetail(generics.RetrieveAPIView):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversitySerializer
    lookup_field = 'slug'


class UniversityList(generics.ListAPIView):
    serializer_class = serializers.UniversitySerializer

    def get_queryset(self):
        from sNeeds.apps.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        university_list = list(study_info_with_active_consultant_qs.values_list('university_id', flat=True))
        return models.University.objects.filter(id__in=university_list)


class FieldOfStudyDetail(generics.RetrieveAPIView):
    queryset = models.FieldOfStudy.objects.all()
    serializer_class = serializers.FieldOfStudySerializer
    lookup_field = 'slug'


class FieldOfStudyList(generics.ListAPIView):
    serializer_class = serializers.FieldOfStudySerializer

    def get_queryset(self):
        from sNeeds.apps.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        field_of_study_list = list(study_info_with_active_consultant_qs.values_list('field_of_study__id', flat=True))
        return models.FieldOfStudy.objects.filter(id__in=field_of_study_list)


class StudentDetailedInfoListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    request_serializer_class = StudentDetailedInfoRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return StudentDetailedInfo.objects.none()
        qs = StudentDetailedInfo.objects.filter(user=user)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentDetailedInfoRetrieveUpdateAPIView(custom_generic_apiviews.BaseRetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    request_serializer_class = StudentDetailedInfoRequestSerializer
    permission_classes = (StudentDetailedInfoOwnerOrInteractConsultantOrWithoutUserPermission,)

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UserStudentDetailedInfoRetrieveAPIView(custom_generic_apiviews.BaseRetrieveAPIView):
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    permission_classes = (permissions.IsAuthenticated,
                          StudentDetailedInfoOwnerOrInteractConsultantOrWithoutUserPermission)
    lookup_url_kwarg = 'user_id'
    lookup_field = 'user__id'


class StudentFormApplySemesterYearListAPIView(custom_generic_apiviews.BaseListAPIView):
    queryset = StudentFormApplySemesterYear.objects.all()
    serializer_class = StudentFormApplySemesterYearSerializer


class StudentFormApplySemesterYearRetrieveAPIView(custom_generic_apiviews.BaseRetrieveAPIView):
    lookup_field = 'id'
    queryset = StudentFormApplySemesterYear.objects.all()
    serializer_class = StudentFormApplySemesterYearSerializer


class BasicFormFieldListAPIView(custom_generic_apiviews.BaseListAPIView):
    queryset = BasicFormField.objects.all()
    serializer_class = BasicFormFieldSerializer

    def get_queryset(self):
        query_form_fields = self.request.query_params.getlist('form_field', None)
        if len(query_form_fields) != 0:
            qs = BasicFormField.objects.none()
            for form_field in query_form_fields:
                try:
                    content_type = ContentType.objects.get(app_label='account', model=form_field)
                    temp_ids = content_type.model_class().objects.all().only('id').values_list('id')
                    qs |= BasicFormField.objects.filter(id__in=temp_ids)
                except ContentType.DoesNotExist:
                    pass
        else:
            qs = self.queryset.none()
        return qs


class GMATCertificateListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = models.GMATCertificate.objects.all()
    serializer_class = serializers.GMATCertificateSerializer

    def get_queryset(self):
        user = self.request.user
        qs = models.GMATCertificate.objects.none()
        if not user.is_authenticated:
            return qs
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.GMATCertificate.objects.filter(student_detailed_info=student_detailed_info)
        return qs


class GMATCertificateRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = models.GMATCertificate.objects.all()
    serializer_class = serializers.GMATCertificateSerializer
    permission_classes = [IsGMATCertificateOwnerOrDetailedInfoWithoutUser]


class GRECertificateListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = models.GRECertificate.objects.all()
    serializer_class = serializers.GRECertificateSerializer

    def get_queryset(self):
        user = self.request.user
        qs = models.GRECertificate.objects.none()
        if not user.is_authenticated:
            return qs
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.GRECertificate.objects.filter(student_detailed_info=student_detailed_info)
        return qs


class GRECertificateRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = models.GRECertificate.objects.all()
    serializer_class = serializers.GRECertificateSerializer
    permission_classes = [IsGRECertificateOwnerOrDetailedInfoWithoutUser]


class WantToApplyListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = models.WantToApply.objects.all()
    serializer_class = serializers.WantToApplySerializer
    request_serializer_class = serializers.WantToApplyRequestSerializer

    def get_queryset(self):
        user = self.request.user
        qs = models.WantToApply.objects.none()
        if not user.is_authenticated:
            return qs
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.WantToApply.objects.filter(student_detailed_info=student_detailed_info)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class WantToApplyRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = models.WantToApply.objects.all()
    serializer_class = serializers.WantToApplySerializer
    permission_classes = [IsWantToApplyOwnerOrDetailedInfoWithoutUser]


class PublicationListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    request_serializer_class = serializers.PublicationRequestSerializer

    def get_queryset(self):
        user = self.request.user
        qs = models.Publication.objects.none()
        if not user.is_authenticated:
            return qs
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.Publication.objects.filter(student_detailed_info=student_detailed_info)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PublicationRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    permission_classes = [IsPublicationOwnerOrDetailedInfoWithoutUser]


class StudentDetailedUniversityThroughListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = models.UniversityThrough.objects.all()
    serializer_class = serializers.UniversityThroughSerializer
    request_serializer_class = serializers.UniversityThroughRequestSerializer

    def get_queryset(self):
        user = self.request.user
        qs = models.UniversityThrough.objects.none()
        if not user.is_authenticated:
            return qs
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.UniversityThrough.objects.filter(student_detailed_info=student_detailed_info)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentDetailedUniversityThroughRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = models.UniversityThrough.objects.all()
    serializer_class = serializers.UniversityThroughSerializer
    permission_classes = [IsUniversityThroughOwnerOrDetailedInfoWithoutUser]


class StudentDetailedLanguageCertificateTypeThroughListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = models.LanguageCertificateTypeThrough.objects.all()
    serializer_class = serializers.LanguageCertificateTypeThroughSerializer
    request_serializer_class = serializers.LanguageCertificateTypeThroughRequestSerializer

    def get_queryset(self):
        user = self.request.user
        qs = models.LanguageCertificateTypeThrough.objects.none()
        if not user.is_authenticated:
            return qs
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.LanguageCertificateTypeThrough.objects.filter(student_detailed_info=student_detailed_info)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentDetailedLanguageCertificateTypeThroughRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = models.LanguageCertificateTypeThrough.objects.all()
    serializer_class = serializers.LanguageCertificateTypeThroughSerializer
    permission_classes = [IsLanguageCertificateTypeThroughOwnerOrDetailedInfoWithoutUser]
