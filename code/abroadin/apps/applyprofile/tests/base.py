from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from abroadin.base.mixins.tests import TestBriefMethodMixin

from abroadin.apps.data.applydata.models import GradeChoices

from ...data.globaldata.models import Major, University, Country
from ...data.applydata.models import RegularLanguageCertificate, GREGeneralCertificate, LanguageCertificate, \
    Publication, Education, GradeChoices, Grade, SemesterYear

User = get_user_model()


class ApplyProfileTestBase(APITestCase, TestBriefMethodMixin):

    def setUp(self) -> None:
        super().setUp()

        # ------- Users -------

        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234", first_name="User 1")
        self.user1.is_admin = False
        self.user1.is_email_verified = True
        self.user1.save()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234", first_name="User 2")
        self.user2.is_admin = False
        self.user2.is_email_verified = True
        self.user2.save()

        # ----- Setup ------

        self.client = APIClient()

        # Countries -------
        self.country1 = Country.objects.create(
            name="country1",
            slug="country1",
            search_name="country1",
            picture=None
        )

        self.country2 = Country.objects.create(
            name="country2",
            slug="country2",
            search_name="country2",
            picture=None
        )

        self.country3 = Country.objects.create(
            name="country3",
            slug="country3",
            search_name="country3",
            picture=None
        )

        # Universities -------
        self.university1 = University.objects.create(
            name="university1",
            search_name="university1",
            country=self.country1,
            description="Test desc1",
            picture=None,
            rank=50,
        )

        self.university2 = University.objects.create(
            name="university2",
            search_name="university2",
            country=self.country2,
            description="Test desc2",
            picture=None,
            rank=150,
        )

        self.university3 = University.objects.create(
            name="university3",
            search_name="university3",
            country=self.country2,
            description="Test desc3",
            picture=None,
            rank=200,
        )

        # Field of Studies -------
        self.major1 = Major.objects.create(
            name="field of study1",
            search_name="field of study1",
            description="Test desc1",
        )

        self.major2 = Major.objects.create(
            name="field of study2",
            search_name="field of study2",
            description="Test desc2",
        )

        self.major3 = Major.objects.create(
            name="field of study3",
            search_name="field of study3",
            description="Test desc3",
        )

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

        self.bachelor_grade = Grade.objects.create(
            name=GradeChoices.BACHELOR
        )

        self.master_grade = Grade.objects.create(
            name=GradeChoices.MASTER
        )

        self.phd_grade = Grade.objects.create(
            name=GradeChoices.PHD
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

        self.education4 = Education.objects.create(
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major3,
            graduate_in=2023,
            thesis_title='education4',
            gpa=15.60,
            content_object=self.major2,
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

        self.ielts3 = RegularLanguageCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
            speaking=6.0,
            reading=5.5,
            writing=7.0,
            listening=8,
            overall=8,
            content_object=self.major2,
        )

        self.gre1 = GREGeneralCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.GRE_GENERAL,
            quantitative=145,
            verbal=145,
            analytical_writing=5,
            content_object=self.major1,
        )