from abroadin.apps.applyprofile.models import ApplyProfile, Admission
from abroadin.apps.applyprofile.tests.base import ApplyProfileTestBase
from abroadin.apps.data.globaldata.models import Major, University, Country
from abroadin.apps.data.applydata.models import GREGeneralCertificate, RegularLanguageCertificate, LanguageCertificate, \
    Publication, Education, GradeChoices, Grade, SemesterYear

from ...tests.base import StoreBaseTest
from ..models import ApplyProfileGroup, SoldApplyProfileGroup


class ApplyProfileStoreTestBase(StoreBaseTest):
    def setUp(self):
        StoreBaseTest.setUp(self)

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

        self.applyprofile1 = ApplyProfile.objects.create(
            name='applyprofile1',
            gap=10,
        )

        self.applyprofile2 = ApplyProfile.objects.create(
            name='applyprofile2',
            gap=10,
        )

        self.applyprofile3 = ApplyProfile.objects.create(
            name='applyprofile3',
            gap=10,
        )

        self.applyprofile4 = ApplyProfile.objects.create(
            name='applyprofile4',
            gap=10,
        )

        self.applyprofile5 = ApplyProfile.objects.create(
            name='applyprofile5',
            gap=10,
        )

        self.applyprofile6 = ApplyProfile.objects.create(
            name='applyprofile6',
            gap=10,
        )

        self.applyprofile7 = ApplyProfile.objects.create(
            name='applyprofile7',
            gap=10,
        )

        self.applyprofile8 = ApplyProfile.objects.create(
            name='applyprofile8',
            gap=10,
        )

        self.applyprofile9 = ApplyProfile.objects.create(
            name='applyprofile9',
            gap=10,
        )

        self.admission1for1 = Admission.objects.create(
            apply_profile=self.applyprofile1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=False,
            scholarship=2000,
            enroll_year=2018,
            description='giivbkwfoewvnopibv',
        )

        self.admission2for1 = Admission.objects.create(
            apply_profile=self.applyprofile1,
            major=self.major2,
            grade=self.bachelor_grade,
            destination=self.university2,
            accepted=True,
            scholarship=3000,
            enroll_year=2018,
            description='sdbfspfkknvkv',
        )

        self.admission1for2 = Admission.objects.create(
            apply_profile=self.applyprofile2,
            major=self.major3,
            grade=self.master_grade,
            destination=self.university3,
            accepted=False,
            scholarship=2200,
            enroll_year=2019,
            description='giivbkwfoewvnopibv',
        )

        self.admission2for2 = Admission.objects.create(
            apply_profile=self.applyprofile2,
            major=self.major2,
            grade=self.master_grade,
            destination=self.university2,
            accepted=False,
            scholarship=800,
            enroll_year=2020,
            description='giivbkwfoewvnopibv',
        )

        self.app_profile_group1 = ApplyProfileGroup.objects.create(
            user=self.user1,
            active=True,
            price=4,
        )
        self.app_profile_group1.apply_profiles.set([self.applyprofile1, self.applyprofile2])

        self.app_profile_group2 = ApplyProfileGroup.objects.create(
            user=self.user1,
            active=True,
            price=4,
        )
        self.app_profile_group2.apply_profiles.set([self.applyprofile4, self.applyprofile5, self.applyprofile6])

        self.app_profile_group3 = ApplyProfileGroup.objects.create(
            user=self.user2,
            active=True,
            price=4,
        )
        self.app_profile_group3.apply_profiles.set([self.applyprofile2, self.applyprofile3,
                                                    self.applyprofile4, self.applyprofile5])

        self.sold_app_profile_group1 = SoldApplyProfileGroup.objects.create(
            sold_to=self.user1,
            price=4,
        )

        self.sold_app_profile_group2 = SoldApplyProfileGroup.objects.create(
            sold_to=self.user1,
            price=4,
        )

        self.sold_app_profile_group3 = SoldApplyProfileGroup.objects.create(
            sold_to=self.user2,
            price=4,
        )

        self.sold_app_profile_group1.apply_profiles.set([self.applyprofile1, self.applyprofile2])

        self.sold_app_profile_group2.apply_profiles.set([self.applyprofile4, self.applyprofile5, self.applyprofile6])

        self.sold_app_profile_group3.apply_profiles.set([self.applyprofile2, self.applyprofile3,
                                                         self.applyprofile4, self.applyprofile5])
