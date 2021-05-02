from decimal import Decimal
from random import randint, choice

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from github import Github

from abroadin.apps.data.applydata.models import Education, LanguageCertificate, RegularLanguageCertificate, \
    Publication, GradeChoices
from abroadin.apps.data.applydata.utils import get_toefl_fake_sub_scores_based_on_overall, \
    get_ielts_fake_sub_scores_based_on_overall
from abroadin.apps.data.globaldata.models import University, Major
from abroadin.apps.estimation.estimations.chances import AdmissionChance
from abroadin.apps.estimation.form.models import StudentDetailedInfo

LCType = LanguageCertificate.LanguageCertificateType

User = get_user_model()
PJRC = Publication.JournalReputationChoices
PWAC = Publication.WhichAuthorChoices

global SDI_CT

TESTCASE_UNI_RANK_CHOICES = ['1to20', '21to100', '101to400', '401to1000', '1000above']
RESULT_UNI_RANK_CHOICES = ["0-20", "20-100", "100-400", "+400"]
PUBLICATION_CHOICES = ['Excellent', 'No', 'Very Good', 'Good', 'Medium']
LANGUAGE_CERT_TYPE_CHOICES = ['IELTS']
EDUCATION_GRADE_CHOICES = ['Master', 'Bachelor']

PUBLICATION_CREATION_CREDENTIALS = {
    'Medium': {1: [(PJRC.ONE_TO_THREE, PWAC.FOURTH_OR_MORE), (PJRC.FOUR_TO_TEN, PWAC.FOURTH_OR_MORE)],
               2: [(PJRC.FOUR_TO_TEN, PWAC.FOURTH_OR_MORE), (PJRC.ABOVE_TEN, PWAC.FOURTH_OR_MORE), ],
               3: [(PJRC.ONE_TO_THREE, PWAC.FIRST), (PJRC.ONE_TO_THREE, PWAC.FIRST), ],
               },
    'Good': {1: [(PJRC.ONE_TO_THREE, PWAC.THIRD), (PJRC.ONE_TO_THREE, PWAC.FOURTH_OR_MORE),
                 (PJRC.FOUR_TO_TEN, PWAC.SECOND), (PJRC.FOUR_TO_TEN, PWAC.THIRD),
                 (PJRC.ABOVE_TEN, PWAC.SECOND), (PJRC.ABOVE_TEN, PWAC.THIRD), ],
             2: [(PJRC.FOUR_TO_TEN, PWAC.THIRD), (PJRC.ABOVE_TEN, PWAC.FIRST),
                 (PJRC.ABOVE_TEN, PWAC.SECOND), (PJRC.ABOVE_TEN, PWAC.THIRD), ],
             3: [(PJRC.FOUR_TO_TEN, PWAC.FOURTH_OR_MORE), (PJRC.ABOVE_TEN, PWAC.SECOND)]
             },
    'Very Good': {1: [(PJRC.ONE_TO_THREE, PWAC.FIRST), (PJRC.ONE_TO_THREE, PWAC.SECOND),
                      (PJRC.FOUR_TO_TEN, PWAC.FIRST), (PJRC.ABOVE_TEN, PWAC.FIRST), ],
                  2: [(PJRC.ONE_TO_THREE, PWAC.THIRD), (PJRC.FOUR_TO_TEN, PWAC.FIRST),
                      (PJRC.FOUR_TO_TEN, PWAC.SECOND)],
                  3: [(PJRC.ONE_TO_THREE, PWAC.THIRD), (PJRC.FOUR_TO_TEN, PWAC.THIRD),
                      (PJRC.ABOVE_TEN, PWAC.FIRST)],
                  },
    'Excellent': {2: [(PJRC.ONE_TO_THREE, PWAC.FIRST), (PJRC.ONE_TO_THREE, PWAC.SECOND), ],
                  3: [(PJRC.ONE_TO_THREE, PWAC.FIRST), (PJRC.ONE_TO_THREE, PWAC.SECOND),
                      (PJRC.FOUR_TO_TEN, PWAC.FIRST), (PJRC.FOUR_TO_TEN, PWAC.SECOND), ],
                  },
}

ADMISSION_CHANCE_LABEL_VALUES = {
    'High': 3,
    'Medium': 2,
    'Low': 1,
}


def fill_sdi_ct():
    global SDI_CT
    SDI_CT = ContentType.objects.get(app_label='form', model='studentdetailedinfo')


def get_user():
    obj, created = User.objects.get_or_create(
        email='ttteeessstttuser@gmail.com',
        password='123456789',
        is_email_verified=True,
        defaults={
            'email': 'ttteeessstttuser@gmail.com',
            'password': '123456789',
            'is_email_verified': True,
        })
    return obj


def _get_suitable_grade(grade_text):
    if grade_text.lower() == 'doctorate':
        return GradeChoices.PHD
    elif grade_text.lower() == 'master':
        return GradeChoices.MASTER
    elif grade_text.lower() == 'bachelor':
        return GradeChoices.BACHELOR
    raise Exception("grade is not in right format")


def _get_suitable_lc_type(lc_type_text):
    if lc_type_text.lower() == 'ielts':
        return LCType.IELTS_GENERAL
    elif lc_type_text.lower() in ['toefl', 'ibt', 'pbt']:
        return LCType.TOEFL
    raise Exception("Language certificate type is not in right format")


def _get_lc_sub_scores(lc_type, lc_overall):
    if lc_type == LCType.TOEFL:
        return get_toefl_fake_sub_scores_based_on_overall(lc_overall)
    elif lc_type == LCType.IELTS_GENERAL or lc_type == LCType.IELTS_ACADEMIC:
        return get_ielts_fake_sub_scores_based_on_overall(lc_overall)

    raise Exception('wrong lc type')


def _convert_lc_overall_into_suitable_type(lc_type, lc_overall):
    if lc_type == LCType.TOEFL:
        return int(lc_overall)
    elif lc_type == LCType.IELTS_GENERAL or lc_type == LCType.IELTS_ACADEMIC:
        return float(lc_overall)


def get_uni_around(rank: int) -> University:
    tolerance = int(rank / 5)
    try:
        random_rank = randint(rank - tolerance, rank + tolerance)
        return University.objects.get(rank=random_rank)
    except University.DoesNotExist:
        return get_uni_around(rank)
    except University.MultipleObjectsReturned:
        return University.objects.filter(rank=rank).first()


def get_major() -> Major:
    return Major.objects.first()


def get_some_engineering_major():
    return Major.objects.first()


def get_sdi(user):
    return StudentDetailedInfo.objects.create(
        user=user,
        age=20,
        gender=StudentDetailedInfo.GenderChoices.MALE,
        is_married=True,
        payment_affordability=StudentDetailedInfo.PaymentAffordabilityChoices.LOW,
        prefers_full_fund=True,
        prefers_half_fund=True,
        comment="This is a comment.",
        powerful_recommendation=False,
        related_work_experience=8,
        academic_break=1,
    )


def get_education(sdi: StudentDetailedInfo, raw_grade, gpa, university_rank) -> Education:
    return Education.objects.create(
        object_id=sdi.id,
        content_type=SDI_CT,
        grade=_get_suitable_grade(raw_grade),
        university=get_uni_around(university_rank),
        graduate_in=2020,
        major=get_some_engineering_major(),
        gpa=gpa,
    )


def get_publications(sdi, publications_quality: str):
    if publications_quality == 'No':
        return []

    publications = []
    count = choice(list(PUBLICATION_CREATION_CREDENTIALS[publications_quality].keys()))
    for i in range(0, count):
        wa, jp = choice(PUBLICATION_CREATION_CREDENTIALS[publications_quality][count])
        publications.append(Publication.objects.create(
            content_type=SDI_CT,
            object_id=sdi.id,
            journal_reputation=jp,
            which_author=wa,
            publish_year=2020,
            title=''
        ))
    return publications


def get_language_certificate(sdi, lc_type_text, lc_overall):
    global SDI_CT
    lc_type = _get_suitable_lc_type(lc_type_text)
    lc_overall = _convert_lc_overall_into_suitable_type(lc_type, lc_overall)
    writing, reading, speaking, listening = _get_lc_sub_scores(lc_type, lc_overall)

    if lc_type == LCType.TOEFL:
        lc = RegularLanguageCertificate(
            certificate_type=lc_type,
            object_id=sdi.id,
            content_type=SDI_CT,
            speaking=speaking,
            listening=listening,
            writing=writing,
            reading=reading,
            overall=lc_overall,
        )
        lc

    if lc_type == LCType.IELTS_ACADEMIC or lc_type == LCType.IELTS_GENERAL:
        lc = RegularLanguageCertificate(
            certificate_type=lc_type,
            object_id=sdi.id,
            content_type=SDI_CT,
            speaking=Decimal("%.1f" % speaking),
            listening=Decimal("%.1f" % listening),
            writing=Decimal("%.1f" % writing),
            reading=Decimal("%.1f" % reading),
            overall=Decimal("%.1f" % lc_overall),
        )
        lc
    return lc


def clear_user_data(user):
    global SDI_CT
    try:
        sdi = StudentDetailedInfo.objects.get(user=user)
        Education.objects.filter(content_type=SDI_CT, object_id=sdi.id).delete()
        LanguageCertificate.objects.filter(content_type=SDI_CT, object_id=sdi.id).delete()
        RegularLanguageCertificate.objects.filter(content_type=SDI_CT,
                                                  object_id=sdi.id).delete()
        Publication.objects.filter(content_type=SDI_CT, object_id=sdi.id).delete()
        StudentDetailedInfo.objects.filter(id=sdi.id).delete()
    except StudentDetailedInfo.DoesNotExist:
        pass


def check_test_case(test_case):
    if test_case['Publication'] not in PUBLICATION_CHOICES:
        raise Exception('wrong Publication input')
    if test_case['Language Cert Type'] not in LANGUAGE_CERT_TYPE_CHOICES:
        raise Exception('wrong Language Cert Type input')
    if test_case['Grade'] not in EDUCATION_GRADE_CHOICES:
        raise Exception('wrong Grade input')
    if list(test_case['Chances']['Admission'].keys()) != TESTCASE_UNI_RANK_CHOICES:
        raise Exception('wrong Chances, Admission key input. valid values: {}'.format(str(TESTCASE_UNI_RANK_CHOICES)))
    if list(test_case['Chances']['Fund'].keys()) != TESTCASE_UNI_RANK_CHOICES:
        raise Exception('wrong Chances, Fund key input. valid values: {}'.format(str(TESTCASE_UNI_RANK_CHOICES)))


class AdmissionChanceResultTest(APITestCase):

    def __init__(self, methodName='runTest'):
        self.failures = []
        self.github_access = Github(settings.GITHUB_ORGANIZATION_ACCESS_KEY)
        self.github_admission_chance_repo = \
            self.github_access.get_repo(settings.ADMISSION_CHANCE_CREDENTIALS_REPOSITORY_NAME)
        super().__init__(methodName)

    def test_results(self):
        assert settings.DEBUG, 'This method is allowed to run in Debug mode only'
        if not settings.DEBUG:
            return
        # test_cases = None
        # with open(os.path.join(settings.BASE_DIR,
        #                        'apps/estimation/estimations/admission_chance_test_data/test_data.py'), 'r') as f:
        #     test_cases = eval(f.read())
        test_cases = eval(self.github_admission_chance_repo.get_contents("test_data.py").decoded_content)
        education_attrs = eval(self.github_admission_chance_repo.get_contents("education_attrs.py").decoded_content)
        admission_chance_attrs = eval(
            self.github_admission_chance_repo.get_contents("admission_attrs.py").decoded_content
        )

        # Structure adopted from abroadin.apps.data.applydata.values.values.VALUES_WITH_ATTRS
        values_with_attrs = {
            'education': education_attrs,
            'admission_chance': admission_chance_attrs,
        }

        fill_sdi_ct()

        user = get_user()
        for test_case in test_cases:
            clear_user_data(user)
            try:
                check_test_case(test_case)
                sdi = get_sdi(user)
                education = get_education(sdi, test_case['Grade'], test_case['GPA'], test_case['University Rank'])

                language_certificate = get_language_certificate(sdi, test_case['Language Cert Type'],
                                                                test_case['Language Cert Score'], )
                publications = get_publications(sdi, test_case['Publication'])

                admission_chance = AdmissionChance(sdi)
                data = {
                    "0-20": admission_chance.get_1_to_20_chance(values_with_attrs=values_with_attrs),
                    "20-100": admission_chance.get_21_to_100_chance(values_with_attrs=values_with_attrs),
                    "100-400": admission_chance.get_101_to_400_chance(values_with_attrs=values_with_attrs),
                    "+400": admission_chance.get_401_above_chance(values_with_attrs=values_with_attrs),
                }
                self.check_result(test_case, admission_chance, data)

            except Exception as e:
                raise e
                # self.failures.append('case {}: ' + str(e).format(test_case['id']))

    def check_result(self, test_case, admission_chance, result_data):
        # Admission part
        for i in range(0, len(RESULT_UNI_RANK_CHOICES)):
            returned_result = admission_chance. \
                convert_value_to_label(result_data[RESULT_UNI_RANK_CHOICES[i]]['admission'])
            expected_result = test_case['Chances']['Admission'][TESTCASE_UNI_RANK_CHOICES[i]]

            self.check_test_and_result(test_case, expected_result, returned_result, 'Admission',
                                       TESTCASE_UNI_RANK_CHOICES[i])

        # Fund part
        for i in range(0, len(RESULT_UNI_RANK_CHOICES)):
            returned_result = admission_chance. \
                convert_value_to_label(result_data[RESULT_UNI_RANK_CHOICES[i]]['full_fund'])
            expected_result = test_case['Chances']['Fund'][TESTCASE_UNI_RANK_CHOICES[i]]

            self.check_test_and_result(test_case, expected_result, returned_result, 'Fund',
                                       TESTCASE_UNI_RANK_CHOICES[i])

    def check_test_and_result(self, test_case, expected_result, returned_result, admission_type, uni_rank_range):
        if expected_result != returned_result:
            detail_dict = {
                'id': test_case['id'],
                'admission_type': admission_type,
                'case_university': uni_rank_range,
                'expected_result': expected_result,
                'system_result': returned_result,
                'system_result_is': 'Better' if ADMISSION_CHANCE_LABEL_VALUES[returned_result] >
                                                ADMISSION_CHANCE_LABEL_VALUES[expected_result] else 'Worse',
                '   ': '                                                              ',
            }
            detail_dict.update(test_case)
            del detail_dict['Chances']
            self.failures.append(detail_dict)
