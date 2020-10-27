from . import review_mixins


class StudentDetailedFormReview(
    review_mixins.ReviewUniversityMixin,
    review_mixins.ReviewPublicationMixin,
    review_mixins.ReviewLanguageMixin,
    review_mixins.ReviewAgeMixin,
    review_mixins.ReviewOthersMixin,
):
    def __init__(self, student_detailed_form):
        self.student_detailed_form = student_detailed_form
        self.last_grade = None
        self.last_university_through = None

    def _set_grade(self):
        self.last_grade = self.student_detailed_form.get_last_university_grade()
        self.last_university_through = self.student_detailed_form.get_last_university_through()

    def _rank(self):
        return self.student_detailed_form.rank

    def _rank_among(self):
        return self.student_detailed_form.__class__.objects.all().count()

    def _better_than_percent(self):
        return int((1 - self._rank() / self._rank_among()) * 100)

    def review_all(self):
        self._set_grade()
        data = {
            "student_detailed_info": self.student_detailed_form.id,
            "university_and_gpa": {
                "data": self.review_universities(),
                "value": None if self.last_university_through is None else self.last_university_through.value,
                "value_label": None if self.last_university_through is None else
                self.last_university_through.get_value_label(),
                "university_value": None if self.last_university_through is None else self.last_university_through.university.value,
                "gpa_value": None if self.last_university_through is None else self.last_university_through.gpa_value
            },
            "publication":  self.review_publications(),
            'language': self.review_language_certificates({"IELTS_ACADEMIC", "IELTS_GENERAL", "TOEFL"}),
            "age_and_gap": {
                "data": self.review_age(),
            },
            "others": {
                "data": self.review_others(),
                "value": self.student_detailed_form.others_value
            },
            "total_value": self.student_detailed_form.value,
            "rank": self._rank(),
            "better_than_percent": self._better_than_percent(),
            "rank_among": self._rank_among()
        }

        return data
