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
    LanguageCertificate,
    RegularLanguageCertificate,
    GMATCertificate,
    GREGeneralCertificate,
    GRESubjectCertificate,
    GREBiologyCertificate,
    GREPhysicsCertificate,
    GREPsychologyCertificate,
    DuolingoCertificate,
    Publication,
    Education,
    Grade,)

from .serializers import (
    SemesterYearSerializer,
    LanguageCertificateSerializer,
    GMATCertificateSerializer,
    RegularLanguageCertificateSerializer,
    GREGeneralCertificateSerializer,
    GRESubjectCertificateSerializer,
    GREBiologyCertificateSerializer,
    GREPhysicsCertificateSerializer,
    GREPsychologyCertificateSerializer,
    DuolingoCertificateSerializer,
    PublicationSerializer,
    PublicationRequestSerializer,
    EducationSerializer,
    EducationRequestSerializer,
    GradeSerializer,)

from ...estimation.form.models import SDI_CT


class SemesterYearListAPIView(generics.CListAPIView):
    THIS_YEAR = timezone.now().year
    queryset = SemesterYear.objects.all().filter(year__gte=THIS_YEAR)
    serializer_class = SemesterYearSerializer


# class BasicFormFieldListAPIView(generics.CListAPIView):
#     queryset = BasicFormField.objects.all()
#     serializer_class = BasicFormFieldSerializer
#
#     def get_queryset(self):
#         request = self.request
#         query_form_fields = request.query_params.getlist('form_field', None)
#         if len(query_form_fields) != 0:
#             qs = BasicFormField.objects.none()
#             for form_field in query_form_fields:
#                 try:
#                     content_type = ContentType.objects.get(app_label='account', model=form_field)
#                     temp_ids = content_type.model_class().objects.all().only('id').values_list('id')
#                     qs |= BasicFormField.objects.filter(id__in=temp_ids)
#                 except ContentType.DoesNotExist:
#                     pass
#         else:
#             qs = self.queryset.none()
#
#         return qs


class LanguageCertificateListCreateAPIView(generics.CListCreateAPIView):
    model_class = LanguageCertificate
    # queryset = model_class.objects.all()
    queryset = None
    serializer_class = LanguageCertificateSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = self.queryset.filter(content_type=SDI_CT, object_id=sdi_id)
        return qs


class LanguageCertificateRetrieveDestroyAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = LanguageCertificate
    # queryset = model_class.objects.all()
    queryset = None
    serializer_class = GMATCertificateSerializer


class RegularLanguageCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = RegularLanguageCertificateSerializer


class RegularLanguageCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = RegularLanguageCertificateSerializer


class GMATCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = GMATCertificateSerializer


class GMATCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = GMATCertificateSerializer


class GREGeneralCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = GREGeneralCertificateSerializer


class GREGeneralCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = GREGeneralCertificateSerializer


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


class GREBiologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREBiologyCertificateSerializer


class GREBiologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREBiologyCertificateSerializer


class GREPhysicsCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPhysicsCertificateSerializer


class GREPhysicsCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPhysicsCertificateSerializer


class GREPsychologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPsychologyCertificateSerializer


class GREPsychologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPsychologyCertificateSerializer


class DuolingoCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = DuolingoCertificateSerializer


class DuolingoCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = DuolingoCertificateSerializer


class PublicationListCreateAPIView(generics.CListCreateAPIView):
    queryset = None
    serializer_class = PublicationSerializer
    request_serializer_class = PublicationRequestSerializer

    def get_queryset(self):
        user = self.request.user
        sdi_id = self.request.query_params.get('student-detailed-info', None)
        qs = self.queryset.filter(content_type=SDI_CT, object_id=sdi_id)
        return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PublicationRetrieveDestroyAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = None
    serializer_class = PublicationSerializer


class EducationListAPIView(generics.CListCreateAPIView):
    queryset = None
    serializer_class = EducationSerializer
    request_serializer_class = EducationRequestSerializer

    # def get_queryset(self):
    #     sdi_id = self.request.query_params.get('student-detailed-info', None)
    #     qs = Education.objects.filter(student_detailed_info__id=sdi_id)
    #     return qs

    @swagger_auto_schema(
        request_body=request_serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class EducationDetailAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = None
    serializer_class = EducationSerializer


class GradesListAPIView(generics.CListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class LanguageCertificateTypeListAPIView(EnumViewList):
    enum_class = LanguageCertificate.LanguageCertificateType


class WhichAuthorChoicesListAPIView(EnumViewList):
    enum_class = Publication.WhichAuthorChoices


class PublicationChoicesListAPIView(EnumViewList):
    enum_class = Publication.PublicationChoices


class JournalReputationChoicesListAPIView(EnumViewList):
    enum_class = Publication.JournalReputationChoices


class Akbar(CAPIView):
    def get(self, request):
        from abroadin.apps.estimation.form.tasks import update_student_detailed_info_ranks
        update_student_detailed_info_ranks()
        return Response()
