from pprint import pprint

from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.applydata.models import GradeChoices, LanguageCertificate, Publication

from abroadin.apps.estimation.form.tests.apis.test_base import FormAPITestBase
from abroadin.apps.estimation.form.models import StudentDetailedInfo

User = get_user_model()


class FormAPITests(FormAPITestBase):

    def setUp(self):
        super().setUp()

        self.payload = {
            "age": 22,
            "gender": "Male",
            "is_married": None,
            "resume": None,
            "related_work_experience": 22,
            "academic_break": 19,
            "olympiad": None,
            "want_to_apply": {
                "countries": [self.country1.id, self.country2.id],
                "universities": [self.university1.id, self.university2.id],
                "grades": [self.master_grade.id, self.phd_grade.id],
                "majors": [self.major1.id, self.major2.id],
                "semester_years": [self.semester_year1.id, self.semester_year2.id]
            },
            "educations": [
                {
                    "graduate_in": 2020,
                    "thesis_title": None,
                    "major": self.major3.id,
                    "grade": GradeChoices.BACHELOR.value,
                    "university": self.university2.id,
                    "gpa": "19.00"
                },
                {
                    "graduate_in": 2018,
                    "thesis_title": "Be to che",
                    "major": self.major4.id,
                    "grade": GradeChoices.MASTER.value,
                    "university": self.university5.id,
                    "gpa": "18.00"
                }
            ],
            "publications": [
                {
                    "journal_reputation": Publication.JournalReputationChoices.FOUR_TO_TEN.value,
                    "publish_year": 2020,
                    "which_author": Publication.WhichAuthorChoices.SECOND.value,
                    "type": Publication.PublicationChoices.JOURNAL.value,
                    "title": "sdfsdf"
                },
                {
                    "journal_reputation": Publication.JournalReputationChoices.ONE_TO_THREE.value,
                    "publish_year": 2018,
                    "which_author": Publication.WhichAuthorChoices.FIRST.value,
                    "type": Publication.PublicationChoices.CONFERENCE.value,
                    "title": "ffff"
                }
            ],
            "language_certificates": [
                {
                    'class_type': 'applydata__regularlanguagecertificate',
                    'data': {
                        "is_mock": False,
                        "certificate_type": LanguageCertificate.LanguageCertificateType.TOEFL.value,
                        'speaking': 23,
                        'listening': 23,
                        'writing': 23,
                        'reading': 23,
                        'overall': 102,
                    },
                },
                {
                    'class_type': 'applydata__regularlanguagecertificate',
                    'data': {
                        "is_mock": True,
                        "certificate_type": LanguageCertificate.LanguageCertificateType.IELTS_GENERAL.value,
                        'speaking': 5,
                        'listening': 5,
                        'writing': 5,
                        'reading': 5,
                        'overall': 6,
                    }
                }
            ],
            "payment_affordability": None,
            "prefers_full_fund": None,
            "prefers_half_fund": None,
            "prefers_self_fund": None,
            "comment": "",
            "powerful_recommendation": False,
            "linkedin_url": None,
            "homepage_url": None
        }

    def _test_form_list(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:student-detailed-info-list', *args, **kwargs)

    def _test_form_detail(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:student-detailed-info-detail', *args, **kwargs)

    def _test_form_detail_user_based(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:user-student-detailed-info-detail', *args, **kwargs)

    def test_form_list_post_201(self):
        self.student_detailed_info1.delete()
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED, data=self.payload)

    def test_form_list_post_401_1(self):
        self.student_detailed_info1.delete()
        res = self._test_form_list("post", None, status.HTTP_401_UNAUTHORIZED, data=self.payload)

    def test_form_list_post_403_2(self):
        self.student_detailed_info1.delete()
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED, data=self.payload)

        self._test_form_list("post", self.user1, status.HTTP_403_FORBIDDEN, data=self.payload)

    def test_form_list_post_400(self):
        self.student_detailed_info1.delete()
        self._test_form_list("post", self.user1, status.HTTP_400_BAD_REQUEST)

    def test_form_detail_get_401(self):
        self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id)
        self._test_form_detail("get", None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.student_detailed_info1.id)

    def test_form_detail_get_403(self):
        self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id)
        self._test_form_detail("get", self.user2, status.HTTP_403_FORBIDDEN,
                               reverse_args=self.student_detailed_info1.id)

    def test_form_detail_put_patch_200_native_fields_update(self):
        def _update_all_fields(update_method, update_fields):
            sdi = StudentDetailedInfo.objects.get(user=self.user1)
            data = self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=sdi.id)
            for k, v in update_fields.items():
                data = self._test_form_detail(
                    update_method, self.user1, status.HTTP_200_OK, reverse_args=data['id'], data={k: v},
                )

            obj = StudentDetailedInfo.objects.get(id=data['id'])
            for k in update_fields.keys():
                self.assertEqual(getattr(obj, k), data[k])
                self.assertEqual(getattr(obj, k), update_fields[k])
            obj.delete()

        all_update_fields = {
            "age": 20,
            "gender": 'Female',
            "related_work_experience": 10,
            "academic_break": 43,
            "olympiad": "Foo olympiad",
            "payment_affordability": "Low",
            "prefers_full_fund": True,
            "prefers_half_fund": False,
            "prefers_self_fund": True,
            "comment": "Foo comment",
            "powerful_recommendation": True,
            "linkedin_url": "https://www.linkedin.com/in/foo/",
            "homepage_url": "https://www.foo.com/",
        }

        # _update_all_fields("put", all_update_fields)
        _update_all_fields("patch", all_update_fields)

    def test_form_detail_put_patch_200_educations(self):

        def find_same(_payload_object, _res_data):
            # print('in find same', _payload_object)
            _found = False
            for updated_object in _res_data:
                all_fields_same = True
                for field in _payload_object.keys():
                    updated_object_attribute = updated_object.get(field)
                    # print(f'{field}, {_payload_object.get(field)}, {updated_object_attribute}')
                    if not isinstance(updated_object_attribute, dict) \
                            and updated_object_attribute != _payload_object.get(
                        field):
                        all_fields_same = False
                        # print('avvali', field, _payload_object.get(field), updated_object_attribute)
                        break
                    elif isinstance(updated_object_attribute, dict) and \
                            'id' in updated_object_attribute and \
                            updated_object_attribute['id'] != _payload_object.get(
                        field):
                        all_fields_same = False
                        # print('dovvomi', field, _payload_object.get(field), updated_object_attribute)
                        break
                    elif isinstance(updated_object_attribute, dict) and \
                            'data' in updated_object_attribute and \
                            updated_object_attribute['data'] != _payload_object.get(
                        field):
                        all_fields_same = False
                        # print('sevvomi', field, _payload_object.get(field), updated_object_attribute)
                        break
                if all_fields_same:
                    _found = True
                    break
            return _found

        def update_field_and_check(update_payload):
            self.student_detailed_info1.delete()
            res_data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED, data=self.payload)
            sdi_id = res_data['id']

            for sdi_relative_field in update_payload.keys():

                res_data = self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=sdi_id)

                self.assertEqual(len(res_data[sdi_relative_field]), len(self.payload[sdi_relative_field]))

                res_data_2 = self._test_form_detail("patch", self.user1, status.HTTP_200_OK, reverse_args=sdi_id,
                                                    data={sdi_relative_field: update_payload[sdi_relative_field]})

                self.assertEqual(len(res_data_2[sdi_relative_field]), len(update_payload[sdi_relative_field]))
                for payload_object in update_payload[sdi_relative_field]:
                    found = find_same(payload_object, res_data_2[sdi_relative_field])
                    self.assertTrue(found)
                    # self.assertDictContainsSubset()

                # pprint(update_payload[sdi_relative_field])
                # pprint(res_data_2[sdi_relative_field])

        data = {
            "educations": [
                {
                    "graduate_in": 2013,
                    "thesis_title": None,
                    "major": self.major2.id,
                    "grade": GradeChoices.BACHELOR.value,
                    "university": self.university4.id,
                    "gpa": "19.00"
                },
                {
                    "graduate_in": 2018,
                    "thesis_title": "Be to che hoooy",
                    "major": self.major4.id,
                    "grade": GradeChoices.MASTER.value,
                    "university": self.university5.id,
                    "gpa": "18.00"
                }
            ],
            "publications": [
                {
                    "journal_reputation": Publication.JournalReputationChoices.ABOVE_TEN.value,
                    "publish_year": 2015,
                    "which_author": Publication.WhichAuthorChoices.SECOND.value,
                    "type": Publication.PublicationChoices.JOURNAL.value,
                    "title": "sdfsdf"
                },
                {
                    "journal_reputation": Publication.JournalReputationChoices.ONE_TO_THREE.value,
                    "publish_year": 2018,
                    "which_author": Publication.WhichAuthorChoices.FIRST.value,
                    "type": Publication.PublicationChoices.CONFERENCE.value,
                    "title": "ffff"
                },
                {
                    "journal_reputation": Publication.JournalReputationChoices.ONE_TO_THREE.value,
                    "publish_year": 2019,
                    "which_author": Publication.WhichAuthorChoices.SECOND.value,
                    "type": Publication.PublicationChoices.CONFERENCE.value,
                    "title": "f14"
                }
            ],
            "language_certificates": [
                {
                    'class_type': 'applydata__regularlanguagecertificate',
                    'data': {
                        "is_mock": True,
                        "certificate_type": LanguageCertificate.LanguageCertificateType.TOEFL.value,
                        'speaking': 23,
                        'listening': 23,
                        'writing': 23,
                        'reading': 23,
                        'overall': 102,
                    },
                },
                {
                    'class_type': 'applydata__regularlanguagecertificate',
                    'data': {
                        "is_mock": True,
                        "certificate_type": LanguageCertificate.LanguageCertificateType.IELTS_GENERAL.value,
                        'speaking': 5,
                        'listening': 5,
                        'writing': 5,
                        'reading': 5,
                        'overall': 6,
                    }
                }
            ],
        }

        update_field_and_check(data)

    def test_form_detail_put_patch_200_want_to_apply_update(self):
        self.student_detailed_info1.delete()
        res_data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED, data=self.payload)
        sdi_id = res_data['id']

        data = {
            "want_to_apply": {
                "countries": [self.country3.id],
                "universities": [self.university3.id, self.university2.id],
                "grades": [self.master_grade.id, self.phd_grade.id],
                "majors": [self.major1.id, self.major2.id, self.major3.id],
                "semester_years": [self.semester_year1.id, self.semester_year2.id]
            },
        }

        res_data = self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=sdi_id)

        # self.assertEqual(len(res_data[sdi_relative_field]), len(self.payload[sdi_relative_field]))

        res_data_2 = self._test_form_detail("patch", self.user1, status.HTTP_200_OK, reverse_args=sdi_id,
                                            data=data)
        for field in data['want_to_apply'].keys():
            for sub_attr_id in data['want_to_apply'][field]:
                self.assertIn(sub_attr_id, [o['id'] for o in res_data_2['want_to_apply'][field]], )

    def test_form_detail_put_patch_401(self):
        self._test_form_detail("put", None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.student_detailed_info1.id)
        self._test_form_detail("patch", None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.student_detailed_info1.id)

    def test_form_detail_put_patch_403(self):
        self._test_form_detail("put", self.user2, status.HTTP_403_FORBIDDEN,
                               reverse_args=self.student_detailed_info1.id)
        self._test_form_detail("patch", self.user2, status.HTTP_403_FORBIDDEN,
                               reverse_args=self.student_detailed_info1.id)

    ############################################################################################
    # for User id based view
    ############################################################################################
    def test_form_detail_user_based_put_patch_200_native_fields_update(self):
        def _update_all_fields(update_method, update_fields):
            sdi = StudentDetailedInfo.objects.get(user=self.user1)
            data = self._test_form_detail_user_based("get", self.user1, status.HTTP_200_OK, reverse_args=sdi.user.id)
            for k, v in update_fields.items():
                data = self._test_form_detail_user_based(
                    update_method, self.user1, status.HTTP_200_OK, reverse_args=sdi.user.id, data={k: v},
                )

            obj = StudentDetailedInfo.objects.get(id=data['id'])
            for k in update_fields.keys():
                self.assertEqual(getattr(obj, k), data[k])
                self.assertEqual(getattr(obj, k), update_fields[k])
            obj.delete()

        all_update_fields = {
            "age": 20,
            "gender": 'Female',
            "related_work_experience": 10,
            "academic_break": 43,
            "olympiad": "Foo olympiad",
            "payment_affordability": "Low",
            "prefers_full_fund": True,
            "prefers_half_fund": False,
            "prefers_self_fund": True,
            "comment": "Foo comment",
            "powerful_recommendation": True,
            "linkedin_url": "https://www.linkedin.com/in/foo/",
            "homepage_url": "https://www.foo.com/",
        }

        # _update_all_fields("put", all_update_fields)
        _update_all_fields("patch", all_update_fields)

    def test_form_detail_user_based_put_patch_200_educations(self):

        def find_same(_payload_object, _res_data):
            # print('in find same', _payload_object)
            _found = False
            for updated_object in _res_data:
                all_fields_same = True
                for field in _payload_object.keys():
                    updated_object_attribute = updated_object.get(field)
                    # print(f'{field}, {_payload_object.get(field)}, {updated_object_attribute}')
                    if not isinstance(updated_object_attribute, dict) \
                            and updated_object_attribute != _payload_object.get(
                        field):
                        all_fields_same = False
                        # print('avvali', field, _payload_object.get(field), updated_object_attribute)
                        break
                    elif isinstance(updated_object_attribute, dict) and \
                            'id' in updated_object_attribute and \
                            updated_object_attribute['id'] != _payload_object.get(
                        field):
                        all_fields_same = False
                        # print('dovvomi', field, _payload_object.get(field), updated_object_attribute)
                        break
                    elif isinstance(updated_object_attribute, dict) and \
                            'data' in updated_object_attribute and \
                            updated_object_attribute['data'] != _payload_object.get(
                        field):
                        all_fields_same = False
                        # print('sevvomi', field, _payload_object.get(field), updated_object_attribute)
                        break
                if all_fields_same:
                    _found = True
                    break
            return _found

        def update_field_and_check(update_payload):
            self.student_detailed_info1.delete()
            res_data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED, data=self.payload)
            sdi_user_id = res_data['user']['id']

            for sdi_relative_field in update_payload.keys():

                res_data = self._test_form_detail_user_based("get", self.user1, status.HTTP_200_OK,
                                                             reverse_args=sdi_user_id)

                self.assertEqual(len(res_data[sdi_relative_field]), len(self.payload[sdi_relative_field]))

                res_data_2 = self._test_form_detail_user_based("patch", self.user1, status.HTTP_200_OK,
                                                               reverse_args=sdi_user_id,
                                                               data={sdi_relative_field: update_payload[
                                                                   sdi_relative_field]})

                self.assertEqual(len(res_data_2[sdi_relative_field]), len(update_payload[sdi_relative_field]))
                for payload_object in update_payload[sdi_relative_field]:
                    found = find_same(payload_object, res_data_2[sdi_relative_field])
                    self.assertTrue(found)
                    # self.assertDictContainsSubset()

                # pprint(update_payload[sdi_relative_field])
                # pprint(res_data_2[sdi_relative_field])

        data = {
            "educations": [
                {
                    "graduate_in": 2013,
                    "thesis_title": None,
                    "major": self.major2.id,
                    "grade": GradeChoices.BACHELOR.value,
                    "university": self.university4.id,
                    "gpa": "19.00"
                },
                {
                    "graduate_in": 2018,
                    "thesis_title": "Be to che hoooy",
                    "major": self.major4.id,
                    "grade": GradeChoices.MASTER.value,
                    "university": self.university5.id,
                    "gpa": "18.00"
                }
            ],
            "publications": [
                {
                    "journal_reputation": Publication.JournalReputationChoices.ABOVE_TEN.value,
                    "publish_year": 2015,
                    "which_author": Publication.WhichAuthorChoices.SECOND.value,
                    "type": Publication.PublicationChoices.JOURNAL.value,
                    "title": "sdfsdf"
                },
                {
                    "journal_reputation": Publication.JournalReputationChoices.ONE_TO_THREE.value,
                    "publish_year": 2018,
                    "which_author": Publication.WhichAuthorChoices.FIRST.value,
                    "type": Publication.PublicationChoices.CONFERENCE.value,
                    "title": "ffff"
                },
                {
                    "journal_reputation": Publication.JournalReputationChoices.ONE_TO_THREE.value,
                    "publish_year": 2019,
                    "which_author": Publication.WhichAuthorChoices.SECOND.value,
                    "type": Publication.PublicationChoices.CONFERENCE.value,
                    "title": "f14"
                }
            ],
            "language_certificates": [
                {
                    'class_type': 'applydata__regularlanguagecertificate',
                    'data': {
                        "is_mock": True,
                        "certificate_type": LanguageCertificate.LanguageCertificateType.TOEFL.value,
                        'speaking': 23,
                        'listening': 23,
                        'writing': 23,
                        'reading': 23,
                        'overall': 102,
                    },
                },
                {
                    'class_type': 'applydata__regularlanguagecertificate',
                    'data': {
                        "is_mock": True,
                        "certificate_type": LanguageCertificate.LanguageCertificateType.IELTS_GENERAL.value,
                        'speaking': 5,
                        'listening': 5,
                        'writing': 5,
                        'reading': 5,
                        'overall': 6,
                    }
                }
            ],
        }

        update_field_and_check(data)

    def test_form_detail_user_based_put_patch_200_want_to_apply_update(self):
        self.student_detailed_info1.delete()
        res_data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED, data=self.payload)
        sdi_user_id = res_data['user']['id']

        data = {
            "want_to_apply": {
                "countries": [self.country3.id],
                "universities": [self.university3.id, self.university2.id],
                "grades": [self.master_grade.id, self.phd_grade.id],
                "majors": [self.major1.id, self.major2.id, self.major3.id],
                "semester_years": [self.semester_year1.id, self.semester_year2.id]
            },
        }

        res_data = self._test_form_detail_user_based("get", self.user1, status.HTTP_200_OK,
                                                     reverse_args=sdi_user_id)

        # self.assertEqual(len(res_data[sdi_relative_field]), len(self.payload[sdi_relative_field]))

        res_data_2 = self._test_form_detail_user_based("patch", self.user1, status.HTTP_200_OK,
                                                       reverse_args=sdi_user_id, data=data)
        for field in data['want_to_apply'].keys():
            for sub_attr_id in data['want_to_apply'][field]:
                self.assertIn(sub_attr_id, [o['id'] for o in res_data_2['want_to_apply'][field]], )

    def test_form_detail_user_based_put_patch_401(self):
        self._test_form_detail_user_based("put", None, status.HTTP_401_UNAUTHORIZED,
                                          reverse_args=self.student_detailed_info1.user.id)
        self._test_form_detail_user_based("patch", None, status.HTTP_401_UNAUTHORIZED,
                                          reverse_args=self.student_detailed_info1.user.id)

    def test_form_detail_user_based_put_patch_403(self):
        self._test_form_detail_user_based("put", self.user2, status.HTTP_403_FORBIDDEN,
                                          reverse_args=self.student_detailed_info1.user.id)
        self._test_form_detail_user_based("patch", self.user2, status.HTTP_403_FORBIDDEN,
                                          reverse_args=self.student_detailed_info1.user.id)
