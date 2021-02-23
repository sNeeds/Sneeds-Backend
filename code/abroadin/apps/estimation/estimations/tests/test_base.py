from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.tests.base import EstimationBaseTest
from abroadin.apps.estimation.form.models import StudentDetailedInfo, Grade, WantToApply, SemesterYear, \
    Education, GradeChoices, Publication, RegularLanguageCertificate, LanguageCertificate
from abroadin.apps.data.globaldata.models import Country, University, Major

User = get_user_model()


class EstimationsAppBaseTests(EstimationBaseTest):

    def setUp(self):
        super().setUp()

        self.app_form_1 = StudentDetailedInfo.objects.create(
            user=self.user1,
            age=27,
            gender=StudentDetailedInfo.GenderChoices.MALE,
            is_married=False,
            payment_affordability=StudentDetailedInfo.PaymentAffordabilityChoices.AVERAGE,
            prefers_full_fund=True,
            prefers_half_fund=True,
            prefers_self_fund=False,
            comment="Foo comment",
            powerful_recommendation=True,
            linkedin_url="https://www.linkedin.com/in/arya-khaligh/",
            homepage_url="http://aryakhaligh.ir/",
        )

        self.app_form_1_university_through_1 = Education.objects.create(
            student_detailed_info=self.app_form_1,
            university=self.university1,
            grade=GradeChoices.BACHELOR,
            major=self.major1,
            graduate_in=2021,
            thesis_title="Foo thesis",
            gpa=17
        )

        self.app_form_1_university_through_2 = Education.objects.create(
            student_detailed_info=self.app_form_1,
            university=self.university1,
            grade=GradeChoices.MASTER,
            major=self.major1,
            graduate_in=2024,
            thesis_title="Foo thesis",
            gpa=17.5
        )

        self.app_form_1_want_to_apply_1 = WantToApply.objects.create(
            student_detailed_info=self.app_form_1,
        )
        self.app_form_1_want_to_apply_1.countries.set(
            Country.objects.filter(id__in=[self.country1.id, self.country2.id]),
        )
        self.app_form_1_want_to_apply_1.universities.set(
            University.objects.filter(id__in=[self.university1.id, self.university2.id]),
        )
        self.app_form_1_want_to_apply_1.grades.set(
            Grade.objects.filter(id__in=[Grade.objects.get(name=GradeChoices.PHD).id]),
        )
        self.app_form_1_want_to_apply_1.majors.set(
            Major.objects.filter(id__in=[self.major1.id, self.major2.id])
        )
        self.app_form_1_want_to_apply_1.semester_years.set(
            SemesterYear.objects.filter(id__in=[self.semester_year1.id, self.semester_year2.id])
        )

        self.app_form_1_publication_1 = Publication.objects.create(
            student_detailed_info=self.app_form_1,
            title="Foo title",
            publish_year=2020,
            which_author=Publication.WhichAuthorChoices.SECOND,
            type=Publication.PublicationChoices.JOURNAL,
            journal_reputation=Publication.JournalReputationChoices.FOUR_TO_TEN
        )

        self.app_form_1_publication_2 = Publication.objects.create(
            student_detailed_info=self.app_form_1,
            title="Foo title",
            publish_year=2020,
            which_author=Publication.WhichAuthorChoices.FIRST,
            type=Publication.PublicationChoices.JOURNAL,
            journal_reputation=Publication.JournalReputationChoices.ABOVE_TEN
        )

        self.app_form_1_language_certificate_1 = RegularLanguageCertificate.objects.create(
            student_detailed_info=self.app_form_1,
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC,
            is_mock=False,
            speaking=7,
            listening=6.5,
            reading=7,
            writing=6,
            overall=6.5
        )
        self.app_form_1_language_certificate_2 = RegularLanguageCertificate.objects.create(
            student_detailed_info=self.app_form_1,
            certificate_type=LanguageCertificate.LanguageCertificateType.TOEFL,
            is_mock=True,
            speaking=98,
            listening=95,
            reading=90,
            writing=100,
            overall=96
        )

