from .review_comments import *
from ..account.models import Grade, University, UniversityThrough, LanguageCertificate, Publication, \
    RegularLanguageCertificate, LanguageCertificateType


class StudentDetailedFormReview:
    def __init__(self, student_detailed_form):
        self.student_detailed_form = student_detailed_form
        self.last_grade = None

    def _review_age(self):
        age = self.student_detailed_form.age
        if age in None:
            return None
        elif age > 30:
            return OLD_AGE_REVIEW
        else:
            return None

    def _set_grade(self):
        last_grade = self.last_grade
        university_through = UniversityThrough.objects.filter(
            student_detailed_info=self.student_detailed_form
        )
        if university_through.get_post_doc():
            last_grade = Grade.POST_DOC
        elif university_through.get_phd():
            last_grade = Grade.PHD
        elif university_through.get_master():
            last_grade = Grade.MASTER
        elif university_through.get_bachelor():
            last_grade = Grade.BACHELOR

        self.last_grade = last_grade

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

        # Supports IELTS general, academic and TOEFL
        IELTS_generals = RegularLanguageCertificate.objects.filter(
            student_detailed_info=form,
            certificate_type = LanguageCertificateType.IELTS_ACADEMIC
        )
        IELTS_academic = RegularLanguageCertificate.objects.filter(
            student_detailed_info=form,
            certificate_type=LanguageCertificateType.IELTS_GENERAL
        )


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

    def review_all(self):
        self._set_grade()
        data = {
            "university": {
                "title": "دانشگاه",
                "data": self.review_universities()
            },
            "publication": {
                "title": "مقالات",
                "data": self.review_publications()
            },
            "age": {
                "title": "سن و گپ تحصیلی",
                "data": self.review_age()
            }
        }

        return data
