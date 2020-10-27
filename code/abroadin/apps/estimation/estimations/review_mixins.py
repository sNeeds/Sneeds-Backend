from abroadin.apps.estimation.estimations.classes import ValueRange
from abroadin.apps.estimation.estimations.review_comments import *
from abroadin.apps.estimation.estimations.values import VALUES_WITH_ATTRS
from abroadin.apps.estimation.form.models import LanguageCertificate, RegularLanguageCertificate, UniversityThrough, \
    GradeChoices, Publication


class ReviewAgeMixin:
    def review_age(self):
        age = self.student_detailed_form.age
        form = self.student_detailed_form

        if age is None:
            return AGE_OKAY_MESSAGE

        elif age < 28:
            return AGE_OKAY_MESSAGE

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


class ReviewLanguageMixin:
    def review_language_certificates(self, types: set):
        data = {}
        language_certificates = LanguageCertificate.objects.filter(
            student_detailed_info=self.student_detailed_form
        )

        for t in types:
            data[t.lower()] = None
            language_type = language_certificates.get_from_this_type_or_none(
                getattr(LanguageCertificate.LanguageCertificateType, t.upper())
            )
            if language_type:
                try:
                    obj = RegularLanguageCertificate.objects.get(id=language_type.id)
                    value_range = ValueRange(VALUES_WITH_ATTRS[t.lower() + "_comments"])
                    comment = value_range.find_value_attrs(obj.overall, 'comment')
                    data[t.lower()] = {
                        "comment": comment,
                        "is_mock": obj.is_mock,
                        "value": obj.compute_value()[0],
                        "value_label": obj.compute_value()[1]
                    }
                except RegularLanguageCertificate.DoesNotExist:
                    pass
            if data.get("ielts_general"):
                data["ielts_general"]["comment"] = CHANGE_GENERAL_WITH_ACADEMIC + data["ielts_general"]["comment"]

        data["total_value"] = language_certificates.get_total_value()
        data["total_value_label"] = language_certificates.get_total_value_label()

        return data


class ReviewUniversityMixin:
    def review_universities(self):
        last_grade = self.last_grade
        university_through = UniversityThrough.objects.filter(
            student_detailed_info=self.student_detailed_form
        )

        self._set_grade()

        # User has previous university
        if self.last_grade:
            last_grade_university = university_through.get(grade=self.last_grade)

        data = {
            'phd': None,
            'master': None,
            'bachelor': None
        }

        if last_grade == GradeChoices.PHD:
            # TODO: PHD remained
            pass
        elif last_grade == GradeChoices.MASTER:
            if last_grade_university.university.rank < 850:
                if last_grade_university.gpa <= 14:
                    data['master'] = MASTER_LAST_GRADE_TOP_850_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['master'] = MASTER_LAST_GRADE_TOP_850_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['master'] = MASTER_LAST_GRADE_TOP_850_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['master'] = MASTER_LAST_GRADE_TOP_850_COMMENTS_GPA_ABOVE_18

            elif 850 <= last_grade_university.university.rank <= 1100:
                if last_grade_university.gpa <= 14:
                    data['master'] = MASTER_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['master'] = MASTER_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['master'] = MASTER_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['master'] = MASTER_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_ABOVE_18

            elif 1100 < last_grade_university.university.rank:
                if last_grade_university.gpa <= 14:
                    data['master'] = MASTER_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['master'] = MASTER_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['master'] = MASTER_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['master'] = MASTER_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_ABOVE_18

            bachelor = university_through.get_bachelor()
            if bachelor is not None:
                if bachelor.gpa <= 14:
                    data['bachelor'] = MASTER_WITH_BACHELOR_BAD_GPA
                elif 14 < bachelor.gpa <= 16:
                    data['bachelor'] = MASTER_WITH_BACHELOR_MODERATE_GPA
                elif 16 < bachelor.gpa <= 18:
                    data['bachelor'] = MASTER_WITH_BACHELOR_GOOD_GPA
                elif 18 < bachelor.gpa:
                    data['bachelor'] = MASTER_WITH_BACHELOR_EXCELLENT_GPA

        elif last_grade == GradeChoices.BACHELOR:
            if last_grade_university.university.rank < 850:
                if last_grade_university.gpa <= 14:
                    data['bachelor'] = BACHELOR_LAST_GRADE_TOP_850_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['bachelor'] = BACHELOR_LAST_GRADE_TOP_850_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['bachelor'] = BACHELOR_LAST_GRADE_TOP_850_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['bachelor'] = BACHELOR_LAST_GRADE_TOP_850_COMMENTS_GPA_ABOVE_18

            elif 850 <= last_grade_university.university.rank <= 1100:
                if last_grade_university.gpa <= 14:
                    data['bachelor'] = BACHELOR_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['bachelor'] = BACHELOR_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['bachelor'] = BACHELOR_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['bachelor'] = BACHELOR_LAST_GRADE_BETWEEN_850_1100_COMMENTS_GPA_ABOVE_18

            elif 1100 < last_grade_university.university.rank:
                if last_grade_university.gpa <= 14:
                    data['bachelor'] = BACHELOR_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_UNDER_14
                if 14 < last_grade_university.gpa <= 16:
                    data['bachelor'] = BACHELOR_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_BETWEEN_14_16
                if 16 < last_grade_university.gpa <= 18:
                    data['bachelor'] = BACHELOR_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_BETWEEN_16_18
                if 18 < last_grade_university.gpa:
                    data['bachelor'] = BACHELOR_LAST_GRADE_ABOVE_1100_COMMENTS_GPA_ABOVE_18

        return data


class ReviewPublicationMixin:
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

        data = {
            "comment": None,
            "total_value": None,
            "total_value_label": None
        }
        publications_qs = Publication.objects.filter(student_detailed_info=self.student_detailed_form)

        excellent_publications = publications_qs.filter(value__gte=0.7)
        great_publications = publications_qs.filter(value__gte=0.6, value__lt=0.7)
        good_publications = publications_qs.filter(value__gte=0.5, value__lt=0.6)
        average_publications = publications_qs.filter(value__gte=0.3, value__lt=0.5)
        bad_publications = publications_qs.filter(value__gte=0, value__lt=0.3)

        more_than_one_publications = bool(publications_qs.count())

        # if self.last_grade == GradeChoices.BACHELOR:
        #     if publications_qs.count() == 0:
        #         data = NO_PUBLICATION_BACHELOR
        #     elif publications_qs.count() == 1:
        #         data = ONE_PUBLICATION_BACHELOR
        #     elif publications_qs.count() == 2:
        #         data = TWO_PUBLICATION_BACHELOR
        #     elif publications_qs.count() >= 3:
        #         data = THREE_OR_MORE_PUBLICATION_BACHELOR
        #
        #     if excellent_publications.exists():
        #         data += _add_review(
        #             excellent_publications,
        #             BACHELOR_HAS_EXCELLENT_PUBLICATION_SINGULAR,
        #             HAS_EXCELLENT_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_EXCELLENT_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             BACHELOR_HAS_EXCELLENT_PUBLICATION_PLURAL,
        #             HAS_EXCELLENT_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #     if great_publications.exists():
        #         data += _add_review(
        #             great_publications,
        #             BACHELOR_HAS_GREAT_PUBLICATION_SINGULAR,
        #             HAS_GREAT_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_GREAT_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             BACHELOR_HAS_GREAT_PUBLICATION_PLURAL,
        #             HAS_GREAT_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #     if good_publications.exists():
        #         data += _add_review(
        #             good_publications,
        #             BACHELOR_HAS_GOOD_PUBLICATION_SINGULAR,
        #             HAS_GOOD_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_GOOD_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             BACHELOR_HAS_GOOD_PUBLICATION_PLURAL,
        #             HAS_GOOD_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #     if average_publications.exists():
        #         data += _add_review(
        #             average_publications,
        #             BACHELOR_HAS_AVERAGE_PUBLICATION_SINGULAR,
        #             HAS_AVERAGE_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_AVERAGE_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             BACHELOR_HAS_AVERAGE_PUBLICATION_PLURAL,
        #             HAS_AVERAGE_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #     if bad_publications.exists():
        #         data += _add_review(
        #             bad_publications,
        #             BACHELOR_HAS_BAD_PUBLICATION_SINGULAR,
        #             HAS_BAD_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_BAD_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             BACHELOR_HAS_BAD_PUBLICATION_PLURAL,
        #             HAS_BAD_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #
        # if self.last_grade == GradeChoices.MASTER:
        #     if publications_qs.count() == 0:
        #         data = NO_PUBLICATION_MASTER
        #     elif publications_qs.count() == 1:
        #         data = ONE_PUBLICATION_MASTER
        #     elif publications_qs.count() == 2:
        #         data = TWO_PUBLICATION_MASTER
        #     elif publications_qs.count() == 3:
        #         data = THREE_PUBLICATION_MASTER
        #     elif publications_qs.count() >= 4:
        #         data = FOUR_OR_MORE_PUBLICATION_MASTER
        #
        #     if excellent_publications.exists():
        #         data += _add_review(
        #             excellent_publications,
        #             MASTER_HAS_EXCELLENT_PUBLICATION_SINGULAR,
        #             HAS_EXCELLENT_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_EXCELLENT_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             MASTER_HAS_EXCELLENT_PUBLICATION_PLURAL,
        #             HAS_EXCELLENT_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #     if great_publications.exists():
        #         data += _add_review(
        #             great_publications,
        #             MASTER_HAS_GREAT_PUBLICATION_SINGULAR,
        #             HAS_GREAT_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_GREAT_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             MASTER_HAS_GREAT_PUBLICATION_PLURAL,
        #             HAS_GREAT_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #     if good_publications.exists():
        #         data += _add_review(
        #             good_publications,
        #             MASTER_HAS_GOOD_PUBLICATION_SINGULAR,
        #             HAS_GOOD_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_GOOD_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             MASTER_HAS_GOOD_PUBLICATION_PLURAL,
        #             HAS_GOOD_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #     if average_publications.exists():
        #         data += _add_review(
        #             average_publications,
        #             MASTER_HAS_AVERAGE_PUBLICATION_SINGULAR,
        #             HAS_AVERAGE_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_AVERAGE_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             MASTER_HAS_AVERAGE_PUBLICATION_PLURAL,
        #             HAS_AVERAGE_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        #     if bad_publications.exists():
        #         data += _add_review(
        #             bad_publications,
        #             MASTER_HAS_BAD_PUBLICATION_SINGULAR,
        #             HAS_BAD_PUBLICATION_SINGULAR_NOT_BETWEEN_OTHERS,
        #             HAS_BAD_PUBLICATION_SINGULAR_BETWEEN_OTHERS,
        #             MASTER_HAS_BAD_PUBLICATION_PLURAL,
        #             HAS_BAD_PUBLICATION_PLURAL_BETWEEN_AND_NOT_BETWEEN_OTHERS,
        #             more_than_one_publications
        #         )
        data["total_value"] = publications_qs.qs_total_value_label()
        data["total_value_label"] = publications_qs.qs_total_value_label()
        data["comment"] = "Coming soon"
        return "Coming soon"


class ReviewOthersMixin:
    def _review_recommendation(self):
        if not self.student_detailed_form.powerful_recommendation:
            return NO_POWERFUL_RECOMMENDATION

        return ""

    def _review_work_experience(self):
        form = self.student_detailed_form
        comment = ""
        if form.related_work_experience:
            # TODO:Change
            value_range = ValueRange(VALUES_WITH_ATTRS["work_experience_comments"])
            comment = value_range.find_value_attrs(form.related_work_experience, 'comment')
        return comment

    def review_others(self):
        data = ""

        data += self._review_recommendation()
        data += self._review_work_experience()

        if data == "":
            data = "Since you have powerful recommendation and you don't have work experience we have no comments in this section."

        return data

