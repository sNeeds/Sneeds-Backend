from django.utils import timezone

from abroadin.base.api import generics
from abroadin.base.api.enum_views import EnumViewList

from .models import SemesterYear, LanguageCertificate, Publication, Grade
from .serializers import SemesterYearSerializer, GradeSerializer


class SemesterYearListView(generics.CListAPIView):
    THIS_YEAR = timezone.now().year
    queryset = SemesterYear.objects.all().filter(year__gte=THIS_YEAR)
    serializer_class = SemesterYearSerializer


class GradesListView(generics.CListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class LanguageCertificateTypeListView(EnumViewList):
    include = [LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
               LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
               LanguageCertificate.LanguageCertificateType.TOEFL]


class WhichAuthorChoicesListView(EnumViewList):
    enum_class = Publication.WhichAuthorChoices


class PublicationChoicesListView(EnumViewList):
    enum_class = Publication.PublicationChoices


class JournalReputationChoicesListView(EnumViewList):
    enum_class = Publication.JournalReputationChoices
