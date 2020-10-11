from .review_comments import *
from .review_mixins import ReviewAgeMixin, ReviewLanguageMixin, ReviewUniversityMixin
from sNeeds.apps.estimation.form.models import Publication, UniversityThrough, GradeChoices


class StudentDetailedFormReview(
    ReviewUniversityMixin,

    ReviewLanguageMixin,
    ReviewAgeMixin
):
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

        if data == "":
            data = "Since you have powerful recommendation and you don't have work experience we have no comments in this section."

        return data

    def review_all(self):
        self._set_grade()
        data = {
            "student_detailed_info": self.student_detailed_form.id,
            "university and gpa": {
                "data": self.review_universities(),
                "value": None if self.last_university_through is None else self.last_university_through.value,
                "value_str": None if self.last_university_through is None else
                self.last_university_through.get_value_label(),
                "university_value": None if self.last_university_through is None else self.last_university_through.university.value,
                "gpa_value": None if self.last_university_through is None else self.last_university_through.gpa_value
            },
            "publication": {
                "data": self.review_publications(),
            },
            'language': self.review_language_certificates({"IELTS_ACADEMIC", "IELTS_GENERAL", "TOEFL"}),
            "age and gap": {
                "data": self.review_age(),
            },
            "others": {
                "data": self.review_others(),
                "value": self.student_detailed_form.others_value
            },
            "total_value": self.student_detailed_form.value,
            "rank": 142,
            "rank_among": 1709
        }

        return data
