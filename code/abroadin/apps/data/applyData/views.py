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
# from abroadin.utils.custom.views import custom_generic_apiviews


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
    Grade
)
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
    GradeSerializer
)
# from .permissions import (
#     IsLanguageCertificateOwnerOrDetailedInfoWithoutUser,
#     IsWantToApplyOwnerOrDetailedInfoWithoutUser,
#     IsPublicationOwnerOrDetailedInfoWithoutUser,
#     IsEducationOwnerOrDetailedInfoWithoutUser,
#     OnlyOneFormPermission,
#     SameUserOrNone, UserAlreadyHasForm,
# )


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
    queryset = model_class.objects.all()
    serializer_class = LanguageCertificateSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     sdi_id = self.request.query_params.get('student-detailed-info', None)
    #     qs = self.queryset.filter(student_detailed_info=sdi_id)
    #     # qs = student_detailed_info_many_to_one_qs(user, sdi_id, self.model_class)
    #     return qs


class LanguageCertificateRetrieveDestroyAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = LanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = GMATCertificateSerializer
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class RegularLanguageCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = RegularLanguageCertificateSerializer


class RegularLanguageCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = RegularLanguageCertificate
    queryset = model_class.objects.all()
    serializer_class = RegularLanguageCertificateSerializer
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GMATCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = GMATCertificateSerializer


class GMATCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GMATCertificate
    queryset = model_class.objects.all()
    serializer_class = GMATCertificateSerializer
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREGeneralCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = GREGeneralCertificateSerializer


class GREGeneralCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREGeneralCertificate
    queryset = model_class.objects.all()
    serializer_class = GREGeneralCertificateSerializer
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


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
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREBiologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREBiologyCertificateSerializer


class GREBiologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREBiologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREBiologyCertificateSerializer
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREPhysicsCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPhysicsCertificateSerializer


class GREPhysicsCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREPhysicsCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPhysicsCertificateSerializer
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class GREPsychologyCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPsychologyCertificateSerializer


class GREPsychologyCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = GREPsychologyCertificate
    queryset = model_class.objects.all()
    serializer_class = GREPsychologyCertificateSerializer
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class DuolingoCertificateListCreateAPIView(LanguageCertificateListCreateAPIView):
    model_class = DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = DuolingoCertificateSerializer


class DuolingoCertificateRetrieveDestroyAPIView(LanguageCertificateRetrieveDestroyAPIView):
    lookup_field = 'id'
    model_class = DuolingoCertificate
    queryset = model_class.objects.all()
    serializer_class = DuolingoCertificateSerializer
    # permission_classes = [IsLanguageCertificateOwnerOrDetailedInfoWithoutUser]


class PublicationListCreateAPIView(generics.CListCreateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     sdi_id = self.request.query_params.get('student-detailed-info', None)
    #     # qs = student_detailed_info_many_to_one_qs(user, sdi_id, Publication)
    #     qs = Publication.objects.filter(student_detailed_info_id=sdi_id)
    #     return qs

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={200: serializer_class},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PublicationRetrieveDestroyAPIView(generics.CRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    # permission_classes = [IsPublicationOwnerOrDetailedInfoWithoutUser]


class EducationListAPIView(generics.CListCreateAPIView):
    queryset = Education.objects.all()
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
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    # permission_classes = [IsEducationOwnerOrDetailedInfoWithoutUser]


class GradesListAPIView(generics.CListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class LanguageCertificateTypeListAPIView(EnumViewList):
    enum_class = LanguageCertificate.LanguageCertificateType


class Akbar(CAPIView):
    def get(self, request):
        from abroadin.apps.estimation.form.tasks import update_student_detailed_info_ranks
        update_student_detailed_info_ranks()
        return Response()