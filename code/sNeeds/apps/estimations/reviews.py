from .review_comments import *
from ..account.models import Grade, University, UniversityThrough, LanguageCertificate, Publication


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

            bachelor = university_through.objects.get_bachelor()
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

        if self.student_detailed_form < 28:
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
        language_certificate_qs = LanguageCertificate.objects.filter(student_detailed_info=form)
        # TODO: R

    def review_publications(self):
        publications_qs = Publication.objects.filter(student_detailed_info=self.student_detailed_form)

        excellent_publications = publications_qs.objects.filter(value__gte=0.7)
        great_publications = publications_qs.objects.filter(value__gte=0.6, value__lt=0.7)
        good_publications = publications_qs.objects.filter(value__gte=0.5, value__lt=0.6)
        average_publications = publications_qs.objects.filter(value__gte=0.3, value__lt=0.5)
        bad_publications = publications_qs.objects.filter(value__gte=0)

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
                pub_count = excellent_publications.count()
                if pub_count == 1:
                    data["کارشناسی"] += BACHELOR_HAS_EXCELLENT_PUBLICATION_SINGULAR
                elif pub_count >= 1:
                    data["کارشناسی"] += BACHELOR_HAS_EXCELLENT_PUBLICATION_PLURAL.replace(
                        "n",
                        NUMBERS_PERSIAN[pub_count]
                    )
            elif great_publications.exists():
                pub_count = great_publications.count()
                if pub_count == 1:
                    data["کارشناسی"] += BACHELOR_HAS_GREAT_PUBLICATION_SINGULAR
                elif pub_count >= 1:
                    data["کارشناسی"] += BACHELOR_HAS_GREAT_PUBLICATION_PLURAL.replace(
                        "n",
                        NUMBERS_PERSIAN[pub_count]
                    )
            elif good_publications.exists():
                pub_count = good_publications.count()
                if pub_count == 1:
                    data["کارشناسی"] += BACHELOR_HAS_GOOD_PUBLICATION_SINGULAR
                elif pub_count >= 1:
                    data["کارشناسی"] += BACHELOR_HAS_GOOD_PUBLICATION_PLURAL.replace(
                        "n",
                        NUMBERS_PERSIAN[pub_count]
                    )
            elif average_publications.exists():
                pub_count = great_publications.count()
                if pub_count == 1:
                    data["کارشناسی"] += BACHELOR_HAS_AVERAGE_PUBLICATION_SINGULAR
                elif pub_count >= 1:
                    data["کارشناسی"] += BACHELOR_HAS_AVERAGE_PUBLICATION_PLURAL.replace(
                        "n",
                        NUMBERS_PERSIAN[pub_count]
                    )
            elif bad_publications.exists():
                pub_count = bad_publications.count()
                if pub_count == 1:
                    data["کارشناسی"] += BACHELOR_HAS_BAD_PUBLICATION_SINGULAR
                elif pub_count >= 1:
                    data["کارشناسی"] += BACHELOR_HAS_BAD_PUBLICATION_PLURAL.replace(
                        "n",
                        NUMBERS_PERSIAN[pub_count]
                    )

    def review_all(self):
        self._set_grade()
        data = {
            "university": {
                "title": "دانشگاه",
                "data": self.review_universities()
            },
            "age": {
                "title": "سن و گپ تحصیلی",
                "data": self.review_age()
            }
        }

        return data
