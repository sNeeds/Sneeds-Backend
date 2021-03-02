from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase

from ..models import Publication, Education, RegularLanguageCertificate, GREGeneralCertificate, Grade, SemesterYear, \
    GradeChoices, LanguageCertificate
from ...globaldata.models import Major, University, Country
from ...globaldata.tests.base import GlobalDataTestBase


class ApplyDataTestBase(GlobalDataTestBase):

    def setUp(self) -> None:

        super().setUp()

        # ------- Semester Years -------

        self.semester_year1 = SemesterYear.objects.create(
            year=2022,
            semester=SemesterYear.SemesterChoices.SPRING
        )
        self.semester_year2 = SemesterYear.objects.create(
            year=2022,
            semester=SemesterYear.SemesterChoices.WINTER
        )
        self.semester_year3 = SemesterYear.objects.create(
            year=2023,
            semester=SemesterYear.SemesterChoices.FALL
        )

        # ------- Grade Objects -------

        self.grade1 = Grade.objects.create(
            name='Grade 1'
        )

        self.grade2 = Grade.objects.create(
            name='Grade 2'
        )

        self.grade3 = Grade.objects.create(
            name='Grade 3'
        )

        self.education1 = Education.objects.create(
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major1,
            graduate_in=2021,
            thesis_title='education1',
            gpa=11.50,
            content_object=self.major1,
        )

        self.education2 = Education.objects.create(
            university=self.university2,
            grade=GradeChoices.MASTER,
            major=self.major2,
            graduate_in=2022,
            thesis_title='education2',
            gpa=12.50,
            content_object=self.major1,
        )

        self.education3 = Education.objects.create(
            university=self.university3,
            grade=GradeChoices.PHD,
            major=self.major3,
            graduate_in=2023,
            thesis_title='education3',
            gpa=13.50,
            content_object=self.major1,
        )

        self.publication1 = Publication.objects.create(
            title="pub1",
            publish_year=2012,
            which_author=Publication.WhichAuthorChoices.FIRST,
            type=Publication.PublicationChoices.JOURNAL,
            journal_reputation=Publication.JournalReputationChoices.ONE_TO_THREE,
            content_object=self.major1,
        )

        self.publication2 = Publication.objects.create(
            title="pub2",
            publish_year=2022,
            which_author=Publication.WhichAuthorChoices.FIRST,
            type=Publication.PublicationChoices.JOURNAL,
            journal_reputation=Publication.JournalReputationChoices.ONE_TO_THREE,
            content_object=self.major1,
        )

        self.publication3 = Publication.objects.create(
            title="pub3",
            publish_year=2032,
            which_author=Publication.WhichAuthorChoices.FIRST,
            type=Publication.PublicationChoices.JOURNAL,
            journal_reputation=Publication.JournalReputationChoices.ONE_TO_THREE,
            content_object=self.major1,
        )

        self.ielts1 = RegularLanguageCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC,
            speaking=6.0,
            reading=5.5,
            writing=7.0,
            listening=8,
            overall=8,
            content_object=self.major1,
        )

        self.ielts2 = RegularLanguageCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
            speaking=6.0,
            reading=5.5,
            writing=7.0,
            listening=8,
            overall=8,
            content_object=self.major1,
        )

        self.gre1 = GREGeneralCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.GRE_GENERAL,
            quantitative=145,
            verbal=145,
            analytical_writing=5,
            content_object=self.major1,
        )
