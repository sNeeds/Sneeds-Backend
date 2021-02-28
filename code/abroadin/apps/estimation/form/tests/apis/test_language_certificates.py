from functools import wraps

from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.applydata import models
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.form.tests.apis.test_base import FormAPITestBase

User = get_user_model()


class LanguageCertificatesAPITest(FormAPITestBase):

    def setUp(self):
        super().setUp()

        self.local_student_detailed_info = StudentDetailedInfo.objects.create()

        self.local_user = User.objects.create_user(email="t1@g.com", password="user1234")

        # id for each case will be generated in create_objects method
        self.info = [
            {'name': 'toefl', 'model': models.RegularLanguageCertificate,
             'list_url_name': 'estimation.form:regular-certificate-list',
             'detail_url_name': 'estimation.form:regular-certificate-detail',
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
             'list_url_name': 'estimation.form:regular-certificate-list',
             'detail_url_name': 'estimation.form:regular-certificate-detail',
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

            {'name': 'ielts_general', 'model': models.RegularLanguageCertificate,
             'list_url_name': 'estimation.form:regular-certificate-list',
             'detail_url_name': 'estimation.form:regular-certificate-detail',
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
             'list_url_name': 'estimation.form:gmat-certificate-list',
             'detail_url_name': 'estimation.form:gmat-certificate-detail',
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
             'list_url_name': 'estimation.form:duolingo-certificate-list',
             'detail_url_name': 'estimation.form:duolingo-certificate-detail',
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
             'list_url_name': 'estimation.form:gre-general-certificate-list',
             'detail_url_name': 'estimation.form:gre-general-certificate-detail',
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
             'list_url_name': 'estimation.form:gre-subject-certificate-list',
             'detail_url_name': 'estimation.form:gre-subject-certificate-detail',
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
             'list_url_name': 'estimation.form:gre-subject-certificate-list',
             'detail_url_name': 'estimation.form:gre-subject-certificate-detail',
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
             'list_url_name': 'estimation.form:gre-biology-certificate-list',
             'detail_url_name': 'estimation.form:gre-biology-certificate-detail',
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
             'list_url_name': 'estimation.form:gre-physics-certificate-list',
             'detail_url_name': 'estimation.form:gre-physics-certificate-detail',
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
             'list_url_name': 'estimation.form:gre-psychology-certificate-list',
             'detail_url_name': 'estimation.form:gre-psychology-certificate-detail',
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

    def create_objects(self):
        for case in self.info:
            case['object'] = case['model'].objects.create(**case['payload'])

    def delete_objects(self):
        for case in self.info:
            del (case['object'])

    def deprecated_test_list_get_200_1(self):
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['list_url_name'],
                                              "get", None, status.HTTP_200_OK,
                                              data={"student-detailed-info": self.local_student_detailed_info.id}
                                              )
            self.assertEqual(len(data), case['response_length'])
        self.delete_objects()

    def deprecated_test_list_get_200_2(self):
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['list_url_name'],
                                              "get", self.local_user, status.HTTP_200_OK,
                                              data={"student-detailed-info": self.local_student_detailed_info.id}
                                              )
            self.assertEqual(len(data), case['response_length'])
        self.delete_objects()

    def deprecated_test_list_get_200_3(self):
        self.create_objects()
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        for case in self.info:
            data = self._endpoint_test_method(case['list_url_name'],
                                              "get", self.local_user, status.HTTP_200_OK,
                                              data={"student-detailed-info": self.local_student_detailed_info.id}
                                              )
            self.assertEqual(len(data), case['response_length'])
        self.delete_objects()

    # TODO sdi with user and it's related things should be protected to not be accessible by other users or
    #  not authenticated clients.
    def deprecated_test_list_get_200_4(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['list_url_name'],
                                              "get", None, status.HTTP_200_OK,
                                              data={"student-detailed-info": self.local_student_detailed_info.id}
                                              )
        self.delete_objects()

    def deprecated_test_list_post_201_1(self):
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['list_url_name'],
                                              "post", None, status.HTTP_201_CREATED,
                                              data=request_data
                                              )

    def deprecated_test_list_post_201_2(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['list_url_name'],
                                              "post", self.local_user, status.HTTP_201_CREATED,
                                              data=request_data
                                              )

    def deprecated_test_list_post_400_1(self):
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['list_url_name'],
                                              "post", self.local_user, status.HTTP_400_BAD_REQUEST,
                                              data=request_data
                                              )

    def deprecated_test_list_post_400_2(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['list_url_name'],
                                              "post", None, status.HTTP_400_BAD_REQUEST,
                                              data=request_data
                                              )

    def deprecated_test_detail_get_200_1(self):
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "get", None, status.HTTP_200_OK,
                                              reverse_args=case['object'].id,
                                              )
        self.delete_objects()

    def deprecated_test_detail_get_200_2(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "get", self.local_user, status.HTTP_200_OK,
                                              reverse_args=case['object'].id,
                                              )
        self.delete_objects()

    def deprecated_test_detail_get_403_1(self):
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "get", self.local_user, status.HTTP_403_FORBIDDEN,
                                              reverse_args=case['object'].id,
                                              )
        self.delete_objects()

    def deprecated_test_detail_get_403_2(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "get", None, status.HTTP_401_UNAUTHORIZED,
                                              reverse_args=case['object'].id,
                                              )
        self.delete_objects()

    def deprecated_test_detail_put_405_1(self):
        self.create_objects()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "put", None, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              reverse_args=case['object'].id,
                                              data=request_data,
                                              )
        self.delete_objects()

    def deprecated_test_detail_put_405_2(self):
        self.create_objects()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "put", self.local_user, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              reverse_args=case['object'].id,
                                              data=request_data,
                                              )
        self.delete_objects()

    def deprecated_test_detail_put_405_3(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "put", None, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              reverse_args=case['object'].id,
                                              data=request_data,
                                              )
        self.delete_objects()

    def deprecated_test_detail_put_405_4(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "put", self.local_user, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              reverse_args=case['object'].id,
                                              data=request_data
                                              )
        self.delete_objects()

    def deprecated_test_detail_patch_405_1(self):
        self.create_objects()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "patch", None, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              reverse_args=case['object'].id,
                                              data=request_data,
                                              )
        self.delete_objects()

    def deprecated_test_detail_patch_405_2(self):
        self.create_objects()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "patch", self.local_user, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              reverse_args=case['object'].id,
                                              data=request_data,
                                              )
        self.delete_objects()

    def deprecated_test_detail_patch_405_3(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "patch", None, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              reverse_args=case['object'].id,
                                              data=request_data,
                                              )
        self.delete_objects()

    def deprecated_test_detail_patch_405_4(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            request_data = case['payload']
            request_data['student_detailed_info'] = request_data['student_detailed_info'].id
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "patch", self.local_user, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              reverse_args=case['object'].id,
                                              data=request_data
                                              )
        self.delete_objects()

    def deprecated_test_detail_delete_204_1(self):
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "delete", None, status.HTTP_204_NO_CONTENT,
                                              reverse_args=case['object'].id,
                                              )

    def deprecated_test_detail_delete_204_2(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "delete", self.local_user, status.HTTP_204_NO_CONTENT,
                                              reverse_args=case['object'].id,
                                              )

    def deprecated_test_detail_delete_403_1(self):
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "delete", self.local_user, status.HTTP_403_FORBIDDEN,
                                              reverse_args=case['object'].id,
                                              )

    def deprecated_test_detail_delete_401_1(self):
        self.local_student_detailed_info.user = self.local_user
        self.local_student_detailed_info.save()
        self.create_objects()
        for case in self.info:
            data = self._endpoint_test_method(case['detail_url_name'],
                                              "delete", None, status.HTTP_401_UNAUTHORIZED,
                                              reverse_args=case['object'].id,
                                              )
