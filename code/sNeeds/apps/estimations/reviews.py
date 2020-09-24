from .review_comments import *
from ..account.models import Grade, University, UniversityThrough, LanguageCertificate, Publication, \
    RegularLanguageCertificate, LanguageCertificateType


class StudentDetailedFormReview:
    def __init__(self, student_detailed_form):
        self.student_detailed_form = student_detailed_form
        self.last_grade = None
        self.last_university_through = None

    def _review_age(self):
        age = self.student_detailed_form.age
        if age in None:
            return None
        elif age > 30:
            return OLD_AGE_REVIEW
        else:
            return None

    def _set_grade(self):
        self.last_grade = self.student_detailed_form.get_last_university_grade()
        self.last_university_through = self.student_detailed_form.get_last_university_through()

    def review_universities(self):
        last_grade = self.last_grade
        university_through = UniversityThrough.objects.filter(
            student_detailed_info=self.student_detailed_form
        )

        self._set_grade()
        # User has no previous university!
        if self.last_grade is None:
            return NONE_UNIVERSITY_COMMENT

        # User has previous university
        last_grade_university = university_through.get(grade=self.last_grade)

        data = {}

        if last_grade == Grade.PHD:
            # TODO: PHD remained
            pass
        elif last_grade == Grade.MASTER:
            if last_grade_university.university.rank < 850:
                if last_grade_university.gpa <= 14:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_TOP_850_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_TOP_850_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_TOP_850_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_TOP_850_COMMENTS_GPA_ABOVE_18

            elif 850 <= last_grade_university.university.rank <= 1100:
                if last_grade_university.gpa <= 14:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_ABOVE_18

            elif 1100 < last_grade_university.university.rank:
                if last_grade_university.gpa <= 14:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['معدل ارشد'] = MASTER_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_ABOVE_18

            bachelor = university_through.get_bachelor()
            if bachelor is not None:
                if bachelor.gpa <= 14:
                    data['معدل کارشناسی'] = MASTER_WITH_BACHELOR_BAD_GPA
                elif 14 < bachelor.gpa <= 16:
                    data['معدل کارشناسی'] = MASTER_WITH_BACHELOR_MODERATE_GPA
                elif 16 < bachelor.gpa <= 18:
                    data['معدل کارشناسی'] = MASTER_WITH_BACHELOR_GOOD_GPA
                elif 18 < bachelor.gpa:
                    data['معدل کارشناسی'] = MASTER_WITH_BACHELOR_EXCELLENT_GPA

        elif last_grade == Grade.BACHELOR:
            if last_grade_university.university.rank < 850:
                if last_grade_university.gpa <= 14:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_TOP_850_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_TOP_850_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_TOP_850_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_TOP_850_COMMENTS_GPA_ABOVE_18

            elif 850 <= last_grade_university.university.rank <= 1100:
                if last_grade_university.gpa <= 14:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_ABOVE_18

            elif 1100 < last_grade_university.university.rank:
                if last_grade_university.gpa <= 14:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['معدل کارشناسی'] = BACHELOR_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_ABOVE_18

        return data

    def review_age(self):
        age = self.student_detailed_form.age
        form = self.student_detailed_form

        if age is None:
            return None

        elif age < 28:
            return None

        elif 28 <= age < 30:
            if form.academic_break is None:
                return AGE_BETWEEN_28_AND_30_WITHOUT_ACADEMIC_BREAK
            elif form.academic_break:
                return AGE_BETWEEN_28_AND_30_WITH_ACADEMIC_BREAK

        elif 30 <= age < 34:
            if form.academic_break is None:
                return AGE_BETWEEN_30_AND_34_WITHOUT_ACADEMIC_BREAK
            elif form.academic_break:
                return AGE_BETWEEN_30_AND_34_WITH_ACADEMIC_BREAK

        elif 34 <= age:
            if form.academic_break is None:
                return AGE_ABOVE_34_WITHOUT_ACADEMIC_BREAK
            elif form.academic_break:
                return AGE_ABOVE_34_WITH_ACADEMIC_BREAK

    def review_language_certificates(self):
        form = self.student_detailed_form

        language_certificates = LanguageCertificate.objects.filter(
            student_detailed_info=form
        )
        # Supports IELTS general, academic and TOEFL
        ielts_academic_qs = RegularLanguageCertificate.objects.filter(
            student_detailed_info=form,
            certificate_type=LanguageCertificateType.IELTS_GENERAL
        )
        ielts_general_qs = RegularLanguageCertificate.objects.filter(
            student_detailed_info=form,
            certificate_type=LanguageCertificateType.IELTS_ACADEMIC
        )
        toefls_qs = RegularLanguageCertificate.objects.filter(
            student_detailed_info=form,
            certificate_type=LanguageCertificateType.TOEFL
        )

        data = {
            "ielts-academic": None,
            "ielts-general": None,
            "toefl": None,
            "total_value": None,
            "total_value_str": None
        }

        if ielts_academic_qs.exists():
            ielts_academic = ielts_academic_qs.first()
            data['ielts_academic'] = {
                "comment": None,
                "is_mock": ielts_academic.is_mock,
                "value": ielts_academic.compute_value()[0],
                "value_str": ielts_academic.compute_value()[1]
            }
            if ielts_academic.overall < 6:
                data["ielts-academic"]["comment"] = IELTS_ACADEMIC_VERY_BAD
            elif 6 <= ielts_academic.overall < 6.5:
                data["ielts-academic"]["comment"] = IELTS_ACADEMIC_BAD
            elif 6.5 <= ielts_academic.overall < 7:
                data["ielts-academic"]["comment"] = IELTS_ACADEMIC_AVERAGE
            elif 7 <= ielts_academic.overall < 7.5:
                data["ielts-academic"]["comment"] = IELTS_ACADEMIC_GOOD
            elif 7.5 <= ielts_academic.overall:
                data["ielts-academic"]["comment"] = IELTS_ACADEMIC_GREAT

        if ielts_general_qs.exists():
            ielts_general = ielts_general_qs.first()
            data['ielts_general'] = {
                "comment": None,
                "is_mock": ielts_general.is_mock,
                "value": ielts_general.compute_value()[0],
                "value_str": ielts_general.compute_value()[1]
            }
            data["ielts-general"]["comment"] = CHANGE_GENERAL_WITH_ACADEMIC
            if ielts_general.overall < 6:
                data["ielts-general"]["comment"] = IELTS_ACADEMIC_VERY_BAD
            elif 6 <= ielts_general.overall < 6.5:
                data["ielts-general"]["comment"] = IELTS_ACADEMIC_BAD
            elif 6.5 <= ielts_general.overall < 7:
                data["ielts-general"]["comment"] = IELTS_ACADEMIC_AVERAGE
            elif 7 <= ielts_general.overall < 7.5:
                data["ielts-general"]["comment"] = IELTS_ACADEMIC_GOOD
            elif 7.5 <= ielts_general.overall:
                data["ielts-general"]["comment"] = IELTS_ACADEMIC_GREAT

        if toefls_qs.exists():
            toefl = toefls_qs.first()
            data['toefl'] = {
                "comment": None,
                "is_mock": toefl.is_mock,
                "value": toefl.compute_value()[0],
                "value_str": toefl.compute_value()[1]
            }
            if toefl.overall < 79:
                data["toefl"]["comment"] = TOEFL_VERY_BAD
            elif 79 <= toefl.overall < 92:
                data["toefl"]["comment"] = TOEFL_BAD
            elif 92 <= toefl.overall < 100:
                data["toefl"]["comment"] = TOEFL_AVERAGE
            elif 100 <= toefl.overall < 110:
                data["toefl"]["comment"] = TOEFL_GOOD
            elif 110 <= toefl.overall:
                data["toefl"]["comment"] = TOEFL_GREAT

        data["total_value"] = language_certificates.get_total_value()[0]
        data["total_value_str"] = language_certificates.get_total_value()[1]

        return data

    def publications_total_value(self):
        publications_qs = Publication.objects.filter(
            student_detailed_info=self.student_detailed_form
        )

        total_value = publications_qs.qs_total_value()

        return total_value

    def publications_total_value_str(self):
        publications_qs = Publication.objects.filter(
            student_detailed_info=self.student_detailed_form
        )

        total_value_str = publications_qs.qs_total_value_str()

        return total_value_str

    def review_publications(self):
        def _get_appended_publication_qs_titles(qs):
            text = ""
            for pub in qs:
                if text == "":
                    text = pub.title
                else:
                    text += " و " + pub.title
            return text

        def _add_review(
                qs,
                singular_comment,
                singular_not_between_others,
                singular_between_others,
                plural_comment,
                plural_between_and_not_between_others,
                more_than_one_pub
        ):
            pub_count = qs.count()
            if pub_count == 1:
                only_pub = qs.first()
                if more_than_one_pub:
                    sentence_start = singular_not_between_others.replace(
                        'x',
                        only_pub.title
                    )
                else:
                    sentence_start = singular_between_others.replace(
                        'x',
                        only_pub.title
                    )
                return sentence_start + singular_comment

            elif pub_count >= 1:
                sentence_start = plural_between_and_not_between_others.replace(
                    "z",
                    _get_appended_publication_qs_titles(qs)
                )
                return sentence_start + plural_comment

        publications_qs = Publication.objects.filter(student_detailed_info=self.student_detailed_form)

        excellent_publications = publications_qs.filter(value__gte=0.7)
        great_publications = publications_qs.filter(value__gte=0.6, value__lt=0.7)
        good_publications = publications_qs.filter(value__gte=0.5, value__lt=0.6)
        average_publications = publications_qs.filter(value__gte=0.3, value__lt=0.5)
        bad_publications = publications_qs.filter(value__gte=0, value__lt=0.3)

        more_than_one_publications = bool(publications_qs.count())

        data = {
            "کارشناسی": None,
            "ارشد": None
        }

        if self.last_grade == Grade.BACHELOR:
            if publications_qs.count() == 0:
                data["کارشناسی"] = NO_PUBLICATION_BACHELOR
            elif publications_qs.count() == 1:
                data["کارشناسی"] = ONE_PUBLICATION_BACHELOR
            elif publications_qs.count() == 2:
                data["کارشناسی"] = TWO_PUBLICATION_BACHELOR
            elif publications_qs.count() >= 3:
                data["کارشناسی"] = THREE_OR_MORE_PUBLICATION_BACHELOR

            if excellent_publications.exists():
                data["کارشناسی"] += _add_review(
                    excellent_publications,
                    BACHELOR_HAS_EXCELLENT_PUBLICATION_SINGULAR,
                    HAS_EXCELLENT_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_EXCELLENT_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    BACHELOR_HAS_EXCELLENT_PUBLICATION_PLURAL,
                    HAS_EXCELLENT_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
            if great_publications.exists():
                data["کارشناسی"] += _add_review(
                    great_publications,
                    BACHELOR_HAS_GREAT_PUBLICATION_SINGULAR,
                    HAS_GREAT_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_GREAT_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    BACHELOR_HAS_GREAT_PUBLICATION_PLURAL,
                    HAS_GREAT_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
            if good_publications.exists():
                data["کارشناسی"] += _add_review(
                    good_publications,
                    BACHELOR_HAS_GOOD_PUBLICATION_SINGULAR,
                    HAS_GOOD_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_GOOD_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    BACHELOR_HAS_GOOD_PUBLICATION_PLURAL,
                    HAS_GOOD_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
            if average_publications.exists():
                data["کارشناسی"] += _add_review(
                    average_publications,
                    BACHELOR_HAS_AVERAGE_PUBLICATION_SINGULAR,
                    HAS_AVERAGE_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_AVERAGE_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    BACHELOR_HAS_AVERAGE_PUBLICATION_PLURAL,
                    HAS_AVERAGE_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
            if bad_publications.exists():
                data["کارشناسی"] += _add_review(
                    bad_publications,
                    BACHELOR_HAS_BAD_PUBLICATION_SINGULAR,
                    HAS_BAD_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_BAD_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    BACHELOR_HAS_BAD_PUBLICATION_PLURAL,
                    HAS_BAD_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )

        if self.last_grade == Grade.MASTER:
            if publications_qs.count() == 0:
                data["ارشد"] = NO_PUBLICATION_MASTER
            elif publications_qs.count() == 1:
                data["ارشد"] = ONE_PUBLICATION_MASTER
            elif publications_qs.count() == 2:
                data["ارشد"] = TWO_PUBLICATION_MASTER
            elif publications_qs.count() == 3:
                data["ارشد"] = THREE_PUBLICATION_MASTER
            elif publications_qs.count() >= 4:
                data["ارشد"] = FOUR_OR_MORE_PUBLICATION_MASTER

            if excellent_publications.exists():
                data["ارشد"] += _add_review(
                    excellent_publications,
                    MASTER_HAS_EXCELLENT_PUBLICATION_SINGULAR,
                    HAS_EXCELLENT_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_EXCELLENT_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    MASTER_HAS_EXCELLENT_PUBLICATION_PLURAL,
                    HAS_EXCELLENT_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
            if great_publications.exists():
                data["ارشد"] += _add_review(
                    great_publications,
                    MASTER_HAS_GREAT_PUBLICATION_SINGULAR,
                    HAS_GREAT_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_GREAT_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    MASTER_HAS_GREAT_PUBLICATION_PLURAL,
                    HAS_GREAT_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
            if good_publications.exists():
                data["ارشد"] += _add_review(
                    good_publications,
                    MASTER_HAS_GOOD_PUBLICATION_SINGULAR,
                    HAS_GOOD_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_GOOD_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    MASTER_HAS_GOOD_PUBLICATION_PLURAL,
                    HAS_GOOD_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
            if average_publications.exists():
                data["ارشد"] += _add_review(
                    average_publications,
                    MASTER_HAS_AVERAGE_PUBLICATION_SINGULAR,
                    HAS_AVERAGE_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_AVERAGE_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    MASTER_HAS_AVERAGE_PUBLICATION_PLURAL,
                    HAS_AVERAGE_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
            if bad_publications.exists():
                data["ارشد"] += _add_review(
                    bad_publications,
                    MASTER_HAS_BAD_PUBLICATION_SINGULAR,
                    HAS_BAD_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
                    HAS_BAD_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
                    MASTER_HAS_BAD_PUBLICATION_PLURAL,
                    HAS_BAD_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
                    more_than_one_publications
                )
        return data

    def _review_recommendation(self):
        if not self.student_detailed_form.powerful_recommendation:
            return NO_POWERFUL_RECOMMENDATION

        return ""

    def _review_work_experience(self):
        form = self.student_detailed_form
        if form.related_work_experience is None:
            return ""
        elif form.related_work_experience < 12:
            return SHORT_WORK_EXPERIENCE
        elif 12 <= form.related_work_experience < 24:
            return AVERAGE_WORK_EXPERIENCE
        elif 24 <= form.related_work_experience:
            return LONG_WORK_EXPERIENCE

    def review_others(self):
        data = ""
        data += self._review_recommendation()
        data += self._review_work_experience()

        return data

    def review_all(self):
        self._set_grade()
        data = {
            "university and gpa": {
                "data": self.review_universities(),
                "value": self.last_university_through.value,
                "value_str": self.last_university_through.compute_value()[1],
                "university_value": self.last_university_through.university.value,
                "gpa_value": self.last_university_through.gpa_value
            },
            "publication": {
                "data": "Coming soon ...",
                "total_value": self.publications_total_value(),
                "total_value_str": self.publications_total_value_str()
            },
            'language': {
                "data": self.review_language_certificates()
            },
            "age": {
                "data": self.review_age(),
            },
            "others": {
                "data": self.review_others(),
                "value": self.student_detailed_form.others_value
            },
            "total_value": self.student_detailed_form.total_value
        }

        return data
