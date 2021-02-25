from abroadin.apps.data.account.tests.fixtures import UniversityFixtures, MajorFixtures
from abroadin.apps.data.applydata.models import SemesterYear, Grade, GradeChoices, Education, Publication, \
    RegularLanguageCertificate, LanguageCertificate, GREGeneralCertificate
from abroadin.base.django.tests.generics import SampleGFKObjectMixIn


class SemesterYearFixtures:
    def setUp(self) -> None:
        super().setUp()

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


class GradeFixtures:

    def setUp(self) -> None:
        super().setUp()

        self.bachelor_grade = Grade.objects.create(
            name=GradeChoices.BACHELOR
        )

        self.master_grade = Grade.objects.create(
            name=GradeChoices.MASTER
        )

        self.phd_grade = Grade.objects.create(
            name=GradeChoices.PHD
        )


class EducationFixtures:

    def setUp(self) -> None:
        super().setUp()

        self.education1 = Education.objects.create(
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major1,
            graduate_in=2021,
            thesis_title='education1',
            gpa=11.50,
            content_object=self.gfk_sample_object1,
        )

        self.education2 = Education.objects.create(
            university=self.university2,
            grade=GradeChoices.MASTER,
            major=self.major2,
            graduate_in=2022,
            thesis_title='education2',
            gpa=12.50,
            content_object=self.gfk_sample_object2,
        )

        self.education3 = Education.objects.create(
            university=self.university3,
            grade=GradeChoices.PHD,
            major=self.major3,
            graduate_in=2023,
            thesis_title='education3',
            gpa=13.50,
            content_object=self.gfk_sample_object3,
        )

        self.education4 = Education.objects.create(
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major3,
            graduate_in=2023,
            thesis_title='education4',
            gpa=15.60,
            content_object=self.gfk_sample_object4,
        )


class PublicationFixtures:

    def setUp(self) -> None:
        super().setUp()

        self.publication1 = Publication.objects.create(
            title="pub1",
            publish_year=2012,
            which_author=Publication.WhichAuthorChoices.FIRST,
            type=Publication.PublicationChoices.JOURNAL,
            journal_reputation=Publication.JournalReputationChoices.ONE_TO_THREE,
            content_object=self.gfk_sample_object1,
        )

        self.publication2 = Publication.objects.create(
            title="pub2",
            publish_year=2022,
            which_author=Publication.WhichAuthorChoices.FIRST,
            type=Publication.PublicationChoices.JOURNAL,
            journal_reputation=Publication.JournalReputationChoices.ONE_TO_THREE,
            content_object=self.gfk_sample_object2,
        )

        self.publication3 = Publication.objects.create(
            title="pub3",
            publish_year=2032,
            which_author=Publication.WhichAuthorChoices.FIRST,
            type=Publication.PublicationChoices.JOURNAL,
            journal_reputation=Publication.JournalReputationChoices.ONE_TO_THREE,
            content_object=self.gfk_sample_object3,
        )


class RegularLCFixtures:

    def setUp(self) -> None:
        super().setUp()

        self.ielts1 = RegularLanguageCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC,
            speaking=6.0,
            reading=5.5,
            writing=7.0,
            listening=8,
            overall=8,
            content_object=self.gfk_sample_object1,
        )

        self.ielts2 = RegularLanguageCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
            speaking=6.0,
            reading=5.5,
            writing=7.0,
            listening=8,
            overall=8,
            content_object=self.gfk_sample_object2,
        )

        self.ielts3 = RegularLanguageCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
            speaking=6.0,
            reading=5.5,
            writing=7.0,
            listening=8,
            overall=8,
            content_object=self.gfk_sample_object3,
        )


class GREGeneralFixtures:

    def setUp(self) -> None:
        super().setUp()

        self.gre1 = GREGeneralCertificate.objects.create(
            certificate_type=LanguageCertificate.LanguageCertificateType.GRE_GENERAL,
            quantitative=145,
            verbal=145,
            analytical_writing=5,
            content_object=self.gfk_sample_object1,
        )
