import uuid

from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity, SearchVector
from django.core.exceptions import ValidationError
from django.db.models import F, Sum, ExpressionWrapper, FloatField
from django.db.models.functions import Length, Ln
from django.utils.translation import ugettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers
from .models import StudentDetailedInfo, StudentFormApplySemesterYear, BasicFormField
from .permissions import IsStudentPermission, \
    StudentDetailedInfoOwnerOrInteractConsultantOrWithoutUserPermission, \
    IsWantToApplyOwnerOrDetailedInfoWithoutUser, IsPublicationOwnerOrDetailedInfoWithoutUser, \
    IsUniversityThroughOwnerOrDetailedInfoWithoutUser, \
    IsLanguageCertificateOwnerOrDetailedInfoWithoutUser
from .serializers import StudentDetailedInfoSerializer, StudentFormApplySemesterYearSerializer, \
    BasicFormFieldSerializer, StudentDetailedInfoRequestSerializer
from sNeeds.utils.custom.views import custom_generic_apiviews


class CountryDetail(generics.RetrieveAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    lookup_field = 'slug'


class CountryList(generics.ListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        request = self.request
        with_time_slot_consultants = request.query_params.get('with-time-slot-consultants', None)
        search_terms = request.query_params.get('search', None)

        qs = models.Country.objects.all()
        other_qs = models.Country.objects. \
            annotate(similarity=TrigramSimilarity('search_name', 'سایر'),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        if with_time_slot_consultants == 'true':
            qs = models.Country.objects.with_active_time_slot_consultants().exclude(slug="iran")

        if search_terms is not None:
            search_term = search_terms[:16]
            if len(search_term) == 0:
                return other_qs

            # To see execution time of queries, use this: python manage.py shell_plus --print-sql
            # To see results use endpoint /form-universities?&search=colombia
            qs = qs.annotate(similarity=TrigramSimilarity('search_name', search_term),
                             search_name_length=Ln(Length('search_name'))). \
                annotate(t=F('similarity') * F('search_name_length')). \
                filter(t__gt=0.4).order_by('-t')

            qs |= other_qs

        qs = qs.distinct()
        return qs


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


class UniversityForFormList(generics.ListAPIView):
    queryset = models.University.objects.none()
    serializer_class = serializers.UniversitySerializer

    def get_queryset(self):
        request = self.request
        params = request.query_params.get('search', '')
        search_terms = params

        other_qs = models.University.objects. \
            annotate(similarity=TrigramSimilarity('search_name', 'سایر'),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        if not search_terms:
            return other_qs

        search_term = search_terms[:16]
        if len(search_term) < 4:
            return other_qs

        # To see execution time of queries, use this: python manage.py shell_plus --print-sql
        # To see results use endpoint /form-universities?&search=colombia
        qs = models.University.objects. \
            annotate(similarity=TrigramSimilarity('search_name', search_term),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        qs = qs | other_qs
        qs = qs.distinct()

        return qs


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


class FieldOfStudyForFormList(generics.ListAPIView):
    queryset = models.FieldOfStudy.objects.none()
    serializer_class = serializers.FieldOfStudySerializer

    def get_queryset(self):
        request = self.request
        params = request.query_params.get('search', '')
        search_terms = params

        other_qs = models.FieldOfStudy.objects. \
            annotate(similarity=TrigramSimilarity('search_name', 'سایر'),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        if not search_terms:
            return other_qs

        search_term = search_terms[:16]
        if len(search_term) < 4:
            return other_qs

        # To see execution time of queries, use this: python manage.py shell_plus --print-sql
        # To see results use endpoint /form-universities?&search=colombia
        qs = models.FieldOfStudy.objects. \
            annotate(similarity=TrigramSimilarity('search_name', search_term),
                     search_name_length=Ln(Length('search_name'))). \
            annotate(t=F('similarity') * F('search_name_length')). \
            filter(t__gt=0.4).order_by('-t')

        qs = qs | other_qs
        qs = qs.distinct()

        return qs


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
        request = self.request
        query_form_fields = request.query_params.getlist('form_field', None)
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


class LanguageCertificateListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    model_class = models.LanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.LanguageCertificateSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = student_detailed_info_many_to_one_qs(user, sdi_id, self.model_class)
        return qs


class LanguageCertificateRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.LanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GMATCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class RegularLanguageCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = models.RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.RegularLanguageCertificateSerializer


class RegularLanguageCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.RegularLanguageCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GMATCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = models.GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GMATCertificateSerializer


class GMATCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GMATCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREGeneralCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = models.GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GREGeneralCertificateSerializer


class GREGeneralCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GREGeneralCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GRESubjectCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = models.GRESubjectCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GRESubjectCertificateSerializer


class GRESubjectCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.GRESubjectCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GRESubjectCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREBiologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = models.GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GREBiologyCertificateSerializer


class GREBiologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GREBiologyCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREPhysicsCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = models.GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GREPhysicsCertificateSerializer


class GREPhysicsCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GREPhysicsCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREPsychologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = models.GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GREPsychologyCertificateSerializer


class GREPsychologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.GREPsychologyCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class DuolingoCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = models.DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.DuolingoCertificateSerializer


class DuolingoCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = models.DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = serializers.DuolingoCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class WantToApplyListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = models.WantToApply.objects.all()
    serializer_class = serializers.WantToApplySerializer
    request_serializer_class = serializers.WantToApplyRequestSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = student_detailed_info_many_to_one_qs(user, sdi_id, models.WantToApply)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class WantToApplyRetrieveUpdateDestroyAPIView(custom_generic_apiviews.BaseRetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = models.WantToApply.objects.all()
    serializer_class = serializers.WantToApplySerializer
    request_serializer_class = serializers.WantToApplyRequestSerializer
    permission_classes = [IsWantToApplyOwnerOrDetailedInfoWithoutUser]

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


class PublicationListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    request_serializer_class = serializers.PublicationRequestSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = student_detailed_info_many_to_one_qs(user, sdi_id, models.Publication)
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
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = student_detailed_info_many_to_one_qs(user, sdi_id, models.UniversityThrough)
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


class GradeChoiceList(custom_generic_apiviews.BaseListAPIView):
    queryset = models.GradeModel.objects.all()
    serializer_class = serializers.GradeModelSerializer


@api_view(['GET'])
def payment_affordability_choices(request, format=None):
    choices = []

    for choice in models.PaymentAffordability:
        choices.append({"value": choice.name, "label": choice.value})

    return Response(
        data={"choices": choices},
        status=status.HTTP_200_OK,
    )


def student_detailed_info_many_to_one_qs(user, sdi_id, model_class):
    if not user.is_authenticated:
        if sdi_id is not None:
            sdi_qs = StudentDetailedInfo.objects.filter(id=sdi_id)
            if sdi_qs.exists():
                sdi = StudentDetailedInfo.objects.get(id=sdi_id)
                if sdi.user is None:
                    qs = model_class.objects.filter(student_detailed_info_id=sdi)
                    return qs
                else:
                    raise exceptions.NotAuthenticated()
            else:
                raise exceptions.NotFound()
        else:
            raise exceptions.NotFound()

    else:
        if sdi_id is not None:
            try:
                sdi_user = StudentDetailedInfo.objects.get(id=sdi_id).user
                if user == sdi_user:
                    qs = model_class.objects.filter(student_detailed_info_id=sdi_id)
                    return qs
                else:
                    raise exceptions.PermissionDenied()
            except StudentDetailedInfo.DoesNotExist:
                raise exceptions.NotFound()
            except ValidationError:
                raise exceptions.ValidationError(detail={"detail": "'{}' is not a valid UUID".format(sdi_id)})

        user_sdi_ids = StudentDetailedInfo.objects.filter(user=user).values_list('id', flat=True)
        qs = model_class.objects.filter(student_detailed_info__in=user_sdi_ids)
        return qs
