from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import TrigramSimilarity
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.models.functions import Length, Ln
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sNeeds.base.api import generics
import sNeeds.apps.estimation.form.models
import sNeeds.apps.estimation.form.serializers
from . import models
from . import serializers
from .models import BasicFormField
from sNeeds.apps.estimation.form.models import StudentFormApplySemesterYear, StudentDetailedInfo
from .permissions import StudentDetailedInfoOwnerOrInteractConsultantOrWithoutUserPermission, \
    IsWantToApplyOwnerOrDetailedInfoWithoutUser, IsPublicationOwnerOrDetailedInfoWithoutUser, \
    IsUniversityThroughOwnerOrDetailedInfoWithoutUser, \
    IsLanguageCertificateOwnerOrDetailedInfoWithoutUser
from sNeeds.apps.estimation.form.serializers import StudentFormApplySemesterYearSerializer, BasicFormFieldSerializer, \
    StudentDetailedInfoSerializer, StudentDetailedInfoRequestSerializer
from sNeeds.utils.custom.views import custom_generic_apiviews


class CountryDetail(generics.CRetrieveAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    lookup_field = 'slug'


class CountryList(generics.CListAPIView):
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


class UniversityDetail(generics.CRetrieveAPIView):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversitySerializer
    lookup_field = 'id'


class UniversityList(generics.CListAPIView):
    serializer_class = serializers.UniversitySerializer

    def get_queryset(self):
        from sNeeds.apps.users.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        university_list = list(study_info_with_active_consultant_qs.values_list('university_id', flat=True))
        return models.University.objects.filter(id__in=university_list)


class UniversityForFormList(generics.CListAPIView):
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


class MajorDetail(generics.CRetrieveAPIView):
    queryset = models.Major.objects.all()
    serializer_class = serializers.MajorSerializer
    lookup_field = 'id'


class MajorList(generics.CListAPIView):
    serializer_class = serializers.MajorSerializer

    def get_queryset(self):
        from sNeeds.apps.users.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        major_list = list(study_info_with_active_consultant_qs.values_list('major__id', flat=True))
        return models.Major.objects.filter(id__in=major_list)


class MajorForFormList(generics.CListAPIView):
    queryset = models.Major.objects.none()
    serializer_class = serializers.MajorSerializer

    def get_queryset(self):
        request = self.request
        params = request.query_params.get('search', '')
        search_terms = params

        other_qs = models.Major.objects. \
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
        qs = models.Major.objects. \
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
    # permission_classes = (StudentDetailedInfoOwnerOrInteractConsultantOrWithoutUserPermission,)

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
    model_class = sNeeds.apps.estimation.form.models.LanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.LanguageCertificateSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = student_detailed_info_many_to_one_qs(user, sdi_id, self.model_class)
        return qs


class LanguageCertificateRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.LanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GMATCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class RegularLanguageCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = sNeeds.apps.estimation.form.models.RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.RegularLanguageCertificateSerializer


class RegularLanguageCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.RegularLanguageCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GMATCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = sNeeds.apps.estimation.form.models.GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GMATCertificateSerializer


class GMATCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GMATCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREGeneralCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = sNeeds.apps.estimation.form.models.GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GREGeneralCertificateSerializer


class GREGeneralCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GREGeneralCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GRESubjectCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = sNeeds.apps.estimation.form.models.GRESubjectCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GRESubjectCertificateSerializer


class GRESubjectCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.GRESubjectCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GRESubjectCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREBiologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = sNeeds.apps.estimation.form.models.GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GREBiologyCertificateSerializer


class GREBiologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GREBiologyCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREPhysicsCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = sNeeds.apps.estimation.form.models.GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GREPhysicsCertificateSerializer


class GREPhysicsCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GREPhysicsCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREPsychologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = sNeeds.apps.estimation.form.models.GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GREPsychologyCertificateSerializer


class GREPsychologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GREPsychologyCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class DuolingoCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = sNeeds.apps.estimation.form.models.DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.DuolingoCertificateSerializer


class DuolingoCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = sNeeds.apps.estimation.form.models.DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.DuolingoCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class WantToApplyListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = sNeeds.apps.estimation.form.models.WantToApply.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.WantToApplySerializer
    request_serializer_class = sNeeds.apps.estimation.form.serializers.WantToApplyRequestSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = student_detailed_info_many_to_one_qs(user, sdi_id, sNeeds.apps.estimation.form.models.WantToApply)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class WantToApplyRetrieveUpdateDestroyAPIView(custom_generic_apiviews.BaseRetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = sNeeds.apps.estimation.form.models.WantToApply.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.WantToApplySerializer
    request_serializer_class = sNeeds.apps.estimation.form.serializers.WantToApplyRequestSerializer
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
    queryset = sNeeds.apps.estimation.form.models.Publication.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.PublicationSerializer
    request_serializer_class = sNeeds.apps.estimation.form.serializers.PublicationRequestSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = student_detailed_info_many_to_one_qs(user, sdi_id, sNeeds.apps.estimation.form.models.Publication)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PublicationRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = sNeeds.apps.estimation.form.models.Publication.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.PublicationSerializer
    permission_classes = [IsPublicationOwnerOrDetailedInfoWithoutUser]


class StudentDetailedUniversityThroughListCreateAPIView(custom_generic_apiviews.BaseListCreateAPIView):
    queryset = sNeeds.apps.estimation.form.models.UniversityThrough.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.UniversityThroughSerializer
    request_serializer_class = sNeeds.apps.estimation.form.serializers.UniversityThroughRequestSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = student_detailed_info_many_to_one_qs(user, sdi_id,
                                                  sNeeds.apps.estimation.form.models.UniversityThrough)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentDetailedUniversityThroughRetrieveDestroyAPIView(custom_generic_apiviews.BaseRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = sNeeds.apps.estimation.form.models.UniversityThrough.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.UniversityThroughSerializer
    permission_classes = [IsUniversityThroughOwnerOrDetailedInfoWithoutUser]


class GradeChoiceList(custom_generic_apiviews.BaseListAPIView):
    queryset = sNeeds.apps.estimation.form.models.GradeModel.objects.all()
    serializer_class = sNeeds.apps.estimation.form.serializers.GradeModelSerializer


@api_view(['GET'])
def payment_affordability_choices(request, format=None):
    choices = []

    for choice in StudentDetailedInfo.PaymentAffordabilityChoices:
        choices.append({"value": choice.value, "label": choice.label})
    # choices = StudentDetailedInfo.PaymentAffordabilityChoices.choices

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
