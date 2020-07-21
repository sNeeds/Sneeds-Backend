from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions

from . import models
from . import serializers
from .models import StudentDetailedInfo, StudentFormApplySemesterYear, BasicFormField
from .permissions import IsStudentPermission, StudentDetailedInfoOwnerOrInteractConsultantPermission, \
    IsGMATCertificateOwner, IsGRECertificateOwner, IsWantToApplyOwner, IsPublicationOwner, IsUniversityThroughOwner
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
    permission_classes = (permissions.IsAuthenticated, IsStudentPermission)

    def get_queryset(self):
        user = self.request.user
        qs = StudentDetailedInfo.objects.filter(user=user)
        return qs


class StudentDetailedInfoRetrieveUpdateAPIView(custom_generic_apiviews.BaseRetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    request_serializer_class = StudentDetailedInfoRequestSerializer
    permission_classes = (permissions.IsAuthenticated, StudentDetailedInfoOwnerOrInteractConsultantPermission)

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
    permission_classes = (permissions.IsAuthenticated, StudentDetailedInfoOwnerOrInteractConsultantPermission)
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
        if query_form_fields is not None:
            qs = BasicFormField.objects.none()
            for form_field in query_form_fields:
                content_type = ContentType.objects.filter(app_label='account', model=form_field)
                if content_type.exists():
                    temp_ids = content_type.first().model_class().objects.all().only('id').values_list('id')
                    qs |= BasicFormField.objects.filter(id__in=temp_ids)
        else:
            qs = self.queryset.all()
        return qs


class GMATCertificateListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    serializer_class = serializers.GMATCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = models.GMATCertificate.objects.none()
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.GMATCertificate.objects.filter(student_detailed_info=student_detailed_info)
        return qs


class GMATCertificateRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    serializer_class = serializers.GMATCertificateSerializer
    permission_classes = [permissions.IsAuthenticated, IsGMATCertificateOwner]


class GRECertificateListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    serializer_class = serializers.GRECertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = models.GRECertificate.objects.none()
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.GRECertificate.objects.filter(student_detailed_info=student_detailed_info)
        return qs


class GRECertificateRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    serializer_class = serializers.GRECertificateSerializer
    permission_classes = [permissions.IsAuthenticated, IsGRECertificateOwner]


class WantToApplyListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    serializer_class = serializers.WantToApplySerializer
    request_serializer_class = serializers.WantToApplyRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = models.WantToApply.objects.none()
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
    serializer_class = serializers.WantToApplySerializer
    permission_classes = [permissions.IsAuthenticated, IsWantToApplyOwner]


class PublicationListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    serializer_class = serializers.PublicationSerializer
    request_serializer_class = serializers.PublicationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = models.Publication.objects.none()
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
    serializer_class = serializers.PublicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsPublicationOwner]


class StudentDetailedUniversityThroughListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    serializer_class = serializers.UniversityThroughSerializer
    request_serializer_class = serializers.UniversityThroughRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = models.UniversityThrough.objects.none()
        student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if student_detailed_info_qs.exists():
            student_detailed_info = student_detailed_info_qs.first()
            qs = models.UniversityThrough.objects.filter(student_detailed_info=student_detailed_info)
        return qs


class StudentDetailedUniversityThroughRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    serializer_class = serializers.UniversityThroughSerializer
    permission_classes = [permissions.IsAuthenticated, IsUniversityThroughOwner]
