import os

from decimal import Decimal
from random import randint

from django.contrib.contenttypes.models import ContentType
from django.db import connections, connection, OperationalError
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from github import Github

from abroadin.apps.data.applydata.models import Grade, Education, LanguageCertificate, RegularLanguageCertificate, \
    Publication, GradeChoices
from abroadin.apps.data.applydata.utils import get_toefl_fake_sub_scores_based_on_overall, \
    get_ielts_fake_sub_scores_based_on_overall
from abroadin.apps.data.globaldata.models import University, Major
from abroadin.apps.estimation.estimations.chances import AdmissionChance
from abroadin.apps.estimation.form.models import StudentDetailedInfo

LCType = LanguageCertificate.LanguageCertificateType

global SDI_CT

User = get_user_model()

github_access = Github(settings.GITHUB_ORGANIZATION_ACCESS_KEY)
repo = github_access.get_repo(settings.ADMISSION_CHANCE_CREDENTIALS_REPOSITORY_NAME)


def create_test_db():
    main_db_name = settings.DATABASES['default']['NAME']
    test_db_name = settings.DATABASES['custom_test_db']['NAME']

    with connection.cursor() as cursor:
        cursor.execute('DROP DATABASE IF EXISTS {} ;'.format(test_db_name))
        try:
            cursor.execute('CREATE DATABASE {} WITH TEMPLATE {};'.format(test_db_name, main_db_name))
        except OperationalError:
            a = cursor.execute(
                "SELECT pid, usename, client_addr FROM pg_stat_activity WHERE datname ='{}';".format(main_db_name))
            print('iiiinja', a)
            cursor.execute('CREATE DATABASE {} WITH TEMPLATE {};'.format(test_db_name, main_db_name))


def fill_sdi_ct():
    global SDI_CT
    SDI_CT = ContentType.objects.using('custom_test_db').get(app_label='form', model='studentdetailedinfo')


def get_user():
    obj, created = User.objects.using('custom_test_db').get_or_create(
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
        return University.objects.using('custom_test_db').get(rank=random_rank)
    except University.DoesNotExist:
        return get_uni_around(rank)
    except University.MultipleObjectsReturned:
        return University.objects.using('custom_test_db').filter(rank=rank).first()


def get_major() -> Major:
    return Major.objects.using('custom_test_db').first()


def get_sdi(user):
    return StudentDetailedInfo.objects.using('custom_test_db').create(
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


def get_some_engineering_major():
    return Major.objects.using('custom_test_db').first()


def get_education(sdi: StudentDetailedInfo, raw_grade, gpa, university_rank) -> Education:
    return Education.objects.using('custom_test_db').create(
        object_id=sdi.id,
        content_type=SDI_CT,
        grade=_get_suitable_grade(raw_grade),
        university=get_uni_around(university_rank),
        graduate_in=2020,
        major=get_some_engineering_major(),
        gpa=gpa,
    )


# def set_publication(sdi, publications_quality):


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
        lc.save(using='custom_test_db')

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
        lc.save(using='custom_test_db')
    return lc


def clear_user_data(user):
    global SDI_CT
    try:
        sdi = StudentDetailedInfo.objects.using('custom_test_db').get(user=user)
        Education.objects.using('custom_test_db').filter(content_type=SDI_CT, object_id=sdi.id).delete()
        LanguageCertificate.objects.using('custom_test_db').filter(content_type=SDI_CT, object_id=sdi.id).delete()
        RegularLanguageCertificate.objects.using('custom_test_db').filter(content_type=SDI_CT,
                                                                          object_id=sdi.id).delete()
        Publication.objects.using('custom_test_db').filter(content_type=SDI_CT, object_id=sdi.id).delete()
        StudentDetailedInfo.objects.using('custom_test_db').filter(id=sdi.id).delete()
    except StudentDetailedInfo.DoesNotExist:
        pass


class AdmissionChanceResultTest(APITestCase):

    def __init__(self, methodName='runTest'):
        self.failures = []
        super().__init__(methodName)

    def test_results(self):

        # test_cases = None
        # with open(os.path.join(settings.BASE_DIR,
        #                        'apps/estimation/estimations/admission_chance_test_data/test_data.py'), 'r') as f:
        #     test_cases = eval(f.read())
        test_cases = eval(repo.get_contents("test_data.py").decoded_content)
        education_attrs = eval(repo.get_contents("education_attrs.py").decoded_content)
        admission_chance_attrs = eval(repo.get_contents("admission_attrs.py").decoded_content)

        # Structure adopted from abroadin.apps.data.applydata.values.values.VALUES_WITH_ATTRS
        values_with_attrs = {
            'education': education_attrs,
            'admission_chance': admission_chance_attrs,
        }

        # create_test_db()
        fill_sdi_ct()

        test_case_uni_rank_keys = ['1to20', '21to100', '101to400', '401to1000', '1000above']
        data_uni_rank_keys = ["0-20", "20-100", "100-400", "+400"]

        user = get_user()

        for test_case in test_cases:
            print(test_case['id'])
            clear_user_data(user)
            try:
                sdi = get_sdi(user)
                education = get_education(sdi, test_case['Grade'], test_case['GPA'], test_case['University Rank'])

                language_certificate = get_language_certificate(sdi, test_case['Language Cert Type'],
                                                                test_case['Language Cert Score'], )
                admission_chance = AdmissionChance(sdi)

                data = {
                    "0-20": admission_chance.get_1_to_20_chance(values_with_attrs=values_with_attrs),
                    "20-100": admission_chance.get_21_to_100_chance(values_with_attrs=values_with_attrs),
                    "100-400": admission_chance.get_101_to_400_chance(values_with_attrs=values_with_attrs),
                    "+400": admission_chance.get_401_above_chance(values_with_attrs=values_with_attrs),
                }

                for i in range(0, len(data_uni_rank_keys)):
                    returned_result = admission_chance.convert_value_to_label(
                        data[data_uni_rank_keys[i]]['admission'])
                    expected_result = test_case['Chances']['Admission'][test_case_uni_rank_keys[i]]

                    if expected_result != returned_result:
                        detail_dict = {
                            'id': test_case['id'],
                            'admission_type': 'Admission',
                            'case_university': test_case_uni_rank_keys[i],
                            'expected_result': expected_result,
                            'returned_result': returned_result,
                            '   ': '                                                              ',
                        }
                        detail_dict.update(test_case)
                        del detail_dict['Chances']
                        self.failures.append(detail_dict)

                for i in range(0, len(data_uni_rank_keys)):
                    returned_result = admission_chance.convert_value_to_label(
                        data[data_uni_rank_keys[i]]['full_fund'])
                    expected_result = test_case['Chances']['Fund'][test_case_uni_rank_keys[i]]

                    if expected_result != returned_result:
                        detail_dict = {
                            'id': test_case['id'],
                            'admission_type': 'Fund',
                            'case_university': test_case_uni_rank_keys[i],
                            'expected_result': expected_result,
                            'returned_result': returned_result,
                            '   ': '                                                              ',
                        }
                        detail_dict.update(test_case)
                        del detail_dict['Chances']
                        self.failures.append(detail_dict)

            except Exception as e:
                raise e
                self.failures.append('case {}: ' + str(e).format(test_case['id']))
        print('finished loop')
