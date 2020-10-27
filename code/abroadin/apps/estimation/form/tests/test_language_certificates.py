from functools import wraps

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.form import models
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.form.tests.apis import FormAPITests

User = get_user_model()


class LanguageCertificatesAPITest(FormAPITests):

    # def _makefunc(self, url, *args, **kwargs):
    #     def result(self, url, )
    #         return self._test_form(url, *args, **kwargs)
    #     # @wraps(val)
    #     # def result(self, url, *args, **kwargs):
    #     #     return self._test_form(url, *args, **kwargs)
    #
    #     return result

    def setUp(self):
        super().setUp()

        self.local_student_detailed_info = StudentDetailedInfo.objects.create()

        self.list_info = [
            {'name': 'toefl', 'model': models.RegularLanguageCertificate,
             'url_name': 'estimation.form:regular-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.TOEFL,
                 'speaking': 23,
                 'listening': 23,
                 'writing': 23,
                 'reading': 23,
                 'overall': 102,
             },
             'response_length': 3,
             },

            {'name': 'ielts_academic', 'model': models.RegularLanguageCertificate,
             'url_name': 'estimation.form:regular-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC,
                 'speaking': 5,
                 'listening': 5,
                 'writing': 5,
                 'reading': 5,
                 'overall': 6,
             },
             'response_length': 3,
             },

            {'name': 'ielts_academic', 'model': models.RegularLanguageCertificate,
             'url_name': 'estimation.form:regular-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
                 'speaking': 5,
                 'listening': 5,
                 'writing': 5,
                 'reading': 5,
                 'overall': 6,
             },
             'response_length': 3,
             },

            {'name': 'gmat', 'model': models.GMATCertificate,
             'url_name': 'estimation.form:gmat-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.GMAT,
                 'analytical_writing_assessment': 4.00,
                 'integrated_reasoning': 3,
                 'quantitative_and_verbal': 34,
                 'total': 350,
             },
             'response_length': 1,
             },

            {'name': 'duolingo', 'model': models.DuolingoCertificate,
             'url_name': 'estimation.form:duolingo-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.DUOLINGO,
                 'overall': 150,
                 'literacy': 40,
                 'comprehension': 40,
                 'conversation': 40,
                 'production': 40,
             },
             'response_length': 1,
             },

            {'name': 'gre_general', 'model': models.GREGeneralCertificate,
             'url_name': 'estimation.form:gre-general-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.GRE_GENERAL,
                 'quantitative': 140,
                 'verbal': 140,
                 'analytical_writing': 4.5,
             },
             'response_length': 1,
             },

            {'name': 'gre_subject', 'model': models.GRESubjectCertificate,
             'url_name': 'estimation.form:gre-subject-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.GRE_CHEMISTRY,
                 'quantitative': 140,
                 'verbal': 140,
                 'analytical_writing': 4.5,
                 'total': 400,
             },
             'response_length': 2,
             },

            {'name': 'gre_subject', 'model': models.GRESubjectCertificate,
             'url_name': 'estimation.form:gre-subject-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.GRE_MATHEMATICS,
                 'quantitative': 140,
                 'verbal': 140,
                 'analytical_writing': 4.5,
                 'total': 400,
             },
             'response_length': 2,
             },

            {'name': 'gre_biology', 'model': models.GREBiologyCertificate,
             'url_name': 'estimation.form:gre-biology-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.GRE_BIOLOGY,
                 'quantitative': 140,
                 'verbal': 140,
                 'analytical_writing': 4.5,
                 'total': 400,
                 'cellular_and_molecular': 40,
                 'organismal': 40,
                 'ecology_and_evolution': 40,
             },
             'response_length': 1,
             },
            {'name': 'gre_physics', 'model': models.GREPhysicsCertificate,
             'url_name': 'estimation.form:gre-physics-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.GRE_PHYSICS,
                 'quantitative': 140,
                 'verbal': 140,
                 'analytical_writing': 4.5,
                 'total': 400,
                 'classical_mechanics': 40,
                 'electromagnetism': 40,
                 'quantum_mechanics': 40,
             },
             'response_length': 1,
             },
            {'name': 'gre_psychology', 'model': models.GREPsychologyCertificate,
             'url_name': 'estimation.form:gre-psychology-certificate-list',
             'payload': {
                 'student_detailed_info': self.local_student_detailed_info,
                 'certificate_type': models.LanguageCertificate.LanguageCertificateType.GRE_PSYCHOLOGY,
                 'quantitative': 140,
                 'verbal': 140,
                 'analytical_writing': 4.5,
                 'total': 400,
                 'biological': 40,
                 'cognitive': 40,
                 'social': 40,
                 'developmental': 40,
                 'clinical': 40,
                 'measurement_or_methodology': 40,
             },
             'response_length': 1,
             },
        ]

        detail_info = [
            {'name': 'toefl', 'model': models.RegularLanguageCertificate,
             'url_name': 'estimation.form:regular-certificate-detail', },
            {'name': 'ielts', 'model': models.RegularLanguageCertificate,
             'url_name': 'estimation.form:regular-certificate-detail', },
            {'name': 'gmat', 'model': models.GMATCertificate,
             'url_name': 'estimation.form:gmat-certificate-detail', },
            {'name': 'duolingo', 'model': models.DuolingoCertificate,
             'url_name': 'estimation.form:duolingo-certificate-detail', },
            {'name': 'gre_general', 'model': models.GREGeneralCertificate,
             'url_name': 'estimation.form:gre-general-certificate-detail', },
            {'name': 'gre_subject', 'model': models.GRESubjectCertificate,
             'url_name': 'estimation.form:gre-subject-certificate-detail', },
            {'name': 'gre_biology', 'model': models.GREBiologyCertificate,
             'url_name': 'estimation.form:gre-biology-certificate-detail', },
            {'name': 'gre_physics', 'model': models.GREPhysicsCertificate,
             'url_name': 'estimation.form:gre-physics-certificate-detail', },
            {'name': 'gre_psychology', 'model': models.GREPsychologyCertificate,
             'url_name': 'estimation.form:gre-psychology-certificate-detail', },
        ]

        for case in self.list_info:
            case['object'] = case['model'].objects.create(**case['payload'])
            # setattr(self, 'local_{}'.format(case['name']), 's')
        # print(list_info)

        data = self._test_form(self.list_info[0]['url_name'],
                               "get", None, status.HTTP_200_OK,
                               )

    def test_list_get_200_1(self):
        for case in self.list_info:
            data = self._test_form(case['url_name'],
                                   "get", None, status.HTTP_200_OK,
                                   data={"student-detailed-info": self.local_student_detailed_info.id}
                                   )
            self.assertEqual(len(data), case['response_length'])
