from . import review_mixins


class StudentDetailedFormReview(
    review_mixins.ReviewUniversityMixin,
    review_mixins.ReviewPublicationMixin,
    review_mixins.ReviewLanguageMixin,
    review_mixins.ReviewAgeAndAcademicBreakMixin,
    review_mixins.ReviewOthersMixin,
):
    def __init__(self, form):
        self.form = form
        self.last_grade = None
        self.last_education = None

    def _set_grade(self):
        self.last_grade = self.form.get_last_university_grade()
        self.last_education = self.form.last_education()

    def _rank(self):
        return self.form.rank

    def _rank_among(self):
        return self.form.__class__.objects.all().count()

    def _better_than_percent(self):
        return int((1 - self._rank() / self._rank_among()) * 100)

    def review_all(self):
        self._set_grade()
        data = {
            "student_detailed_info": self.form.id,

            "university_and_gpa": {
                "comment": self.review_universities(),
                "value": None if self.last_education is None else self.last_education.value,
                "value_label": None if self.last_education is None else
                self.last_education.get_value_label(),
                "university_value": None if self.last_education is None else self.last_education.university.value,
                "gpa_value": None if self.last_education is None else self.last_education.gpa_value
            },

            "publication":  self.review_publications(),

            'language': self.review_language_certificates(
                {"IELTS_ACADEMIC", "IELTS_GENERAL", "TOEFL"}
            ),

            "age_and_gap": {
                "comment": self.review_age_and_academic_break(),
            },

            "others": {
                "comment": self.review_others(),
                "value": self.form.others_value
            },

            "total_value": self.form.value,
            "rank": self._rank(),
            "better_than_percent": self._better_than_percent(),
            "rank_among": self._rank_among()
        }

        return data
