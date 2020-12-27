from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from rest_framework import permissions, status, exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from abroadin.base.api import generics
from abroadin.base.api.enum_views import EnumViewList
from abroadin.base.api.permissions import permission_class_factory

from abroadin.base.api.viewsets import CAPIView

from .models import (
    SemesterYear,
    StudentDetailedInfo,
    GradeChoices,
    BasicFormField,
    LanguageCertificate,
    RegularLanguageCertificate,
    GMATCertificate,
    GREGeneralCertificate,
    GRESubjectCertificate,
    GREBiologyCertificate,
    GREPhysicsCertificate,
    GREPsychologyCertificate,
    DuolingoCertificate,
    WantToApply,
    Publication,
    UniversityThrough,
    Grade
)
from .serializers import (
    SemesterYearSerializer,
    BasicFormFieldSerializer,
    StudentDetailedInfoSerializer,
    StudentDetailedInfoRequestSerializer,
    LanguageCertificateSerializer,
    GMATCertificateSerializer,
    RegularLanguageCertificateSerializer,
    GREGeneralCertificateSerializer,
    GRESubjectCertificateSerializer,
    GREBiologyCertificateSerializer,
    GREPhysicsCertificateSerializer,
    GREPsychologyCertificateSerializer,
    DuolingoCertificateSerializer,
    WantToApplySerializer,
    WantToApplyRequestSerializer,
    PublicationSerializer,
    PublicationRequestSerializer,
    UniversityThroughSerializer,
    UniversityThroughRequestSerializer,
    GradeSerializer
)
from .permissions import (
    IsLanguageCertificateOwnerOrDetailedInfoWithoutUser,
    IsWantToApplyOwnerOrDetailedInfoWithoutUser,
    IsPublicationOwnerOrDetailedInfoWithoutUser,
    IsUniversityThroughOwnerOrDetailedInfoWithoutUser,
    OnlyOneFormPermission,
    SameUserOrNone, UserAlreadyHasForm,
)


class StudentDetailedInfoListCreateAPIView(generics.CListCreateAPIView):
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    request_serializer_class = StudentDetailedInfoRequestSerializer
    permission_classes = [
        permission_class_factory(OnlyOneFormPermission, ["POST"])
    ]

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
    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            super().perform_create(serializer)

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentDetailedInfoRetrieveUpdateAPIView(generics.CRetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    request_serializer_class = StudentDetailedInfoRequestSerializer

    permission_classes = [
        permission_class_factory(SameUserOrNone, ["GET", "PUT", "PATCH"]),
        permission_class_factory(UserAlreadyHasForm, ["PUT", "PATCH"])
    ]

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

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            super().perform_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            request.data.update({"user": user.id})
        return super().partial_update(request, *args, **kwargs)


class UserStudentDetailedInfoRetrieveAPIView(generics.CRetrieveAPIView):
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    lookup_url_kwarg = 'user_id'
    lookup_field = 'user__id'


class SemesterYearListAPIView(generics.CListAPIView):
    THIS_YEAR = timezone.now().year
    queryset = SemesterYear.objects.all().filter(year__gte=THIS_YEAR)
    serializer_class = SemesterYearSerializer


class BasicFormFieldListAPIView(generics.CListAPIView):
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


class LanguageCertificateListCreateAPIView(generics.CListCreateAPIView):
    model_class = LanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = LanguageCertificateSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = self.queryset.filter(student_detailed_info=sdi_id)
        # qs = student_detailed_info_many_to_one_qs(user, sdi_id, self.model_class)
        return qs


class LanguageCertificateRetrieveDestroyAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = LanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = GMATCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class RegularLanguageCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = RegularLanguageCertificateSerializer


class RegularLanguageCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = RegularLanguageCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GMATCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = GMATCertificateSerializer


class GMATCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = GMATCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREGeneralCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = GREGeneralCertificateSerializer


class GREGeneralCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = GREGeneralCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GRESubjectCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GRESubjectCertificate
    separate_sub_certificates = [
        LanguageCertificate.LanguageCertificateType.GRE_PSYCHOLOGY,
        LanguageCertificate.LanguageCertificateType.GRE_BIOLOGY,
        LanguageCertificate.LanguageCertificateType.GRE_PHYSICS,
    ]
    queryset = model_class.objects.all().exclude(certificate_type__in=separate_sub_certificates)
    serializer_class = GRESubjectCertificateSerializer


class GRESubjectCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GRESubjectCertificate
    queryset = model_class.objects.all()
    serializer_class = GRESubjectCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREBiologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREBiologyCertificateSerializer


class GREBiologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREBiologyCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREPhysicsCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPhysicsCertificateSerializer


class GREPhysicsCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPhysicsCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREPsychologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPsychologyCertificateSerializer


class GREPsychologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPsychologyCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class DuolingoCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = DuolingoCertificateSerializer


class DuolingoCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = DuolingoCertificateSerializer
    permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class WantToApplyListAPIView(generics.CListCreateAPIView):
    serializer_class = WantToApplySerializer
    request_serializer_class = WantToApplyRequestSerializer

    def get_queryset(self):
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = WantToApply.objects.filter(student_detailed_info_id=sdi_id)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class WantToApplyDetailAPIView(generics.CRetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = WantToApply.objects.all()
    serializer_class = WantToApplySerializer
    request_serializer_class = WantToApplyRequestSerializer
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


class PublicationListCreateAPIView(generics.CListCreateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    request_serializer_class = PublicationRequestSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        # qs = student_detailed_info_many_to_one_qs(user, sdi_id, Publication)
        qs = Publication.objects.filter(student_detailed_info_id=sdi_id)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PublicationRetrieveDestroyAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsPublicationOwnerOrDetailedInfoWithoutUser]


class UniversityThroughListAPIView(generics.CListCreateAPIView):
    queryset = UniversityThrough.objects.all()
    serializer_class = UniversityThroughSerializer
    request_serializer_class = UniversityThroughRequestSerializer

    def get_queryset(self):
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = UniversityThrough.objects.filter(student_detailed_info__id=sdi_id)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UniversityThroughDetailAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = UniversityThrough.objects.all()
    serializer_class = UniversityThroughSerializer
    permission_classes = [IsUniversityThroughOwnerOrDetailedInfoWithoutUser]


class GradesListAPIView(generics.CListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class WhichAuthorChoicesListAPIView(EnumViewList):
    enum_class = Publication.WhichAuthorChoices


class PublicationChoicesListAPIView(EnumViewList):
    enum_class = Publication.PublicationChoices


class JournalReputationChoicesListAPIView(EnumViewList):
    enum_class = Publication.JournalReputationChoices


class PaymentAffordabilityChoicesListAPIView(EnumViewList):
    enum_class = StudentDetailedInfo.PaymentAffordabilityChoices


class GenderChoicesListAPIView(EnumViewList):
    enum_class = StudentDetailedInfo.GenderChoices


class LanguageCertificateTypeListAPIView(EnumViewList):
    enum_class = LanguageCertificate.LanguageCertificateType


class Akbar(CAPIView):
    def get(self, request):
        from abroadin.apps.estimation.form.tasks import update_student_detailed_info_ranks
        update_student_detailed_info_ranks()
        return Response()