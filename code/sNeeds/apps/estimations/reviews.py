from .review_comments import *
from ..account.models import Grade, University, UniversityThrough


class StudentDetailedFormReview:
    def __init__(self, student_detailed_form):
        self.student_detailed_form = student_detailed_form
        self.last_grade = None

    def _review_age(self):
        age = self.student_detailed_form.age
        if age in None
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
        if university_through.objects.get_post_docs().exists():
            last_grade = Grade.POST_DOC
        elif university_through.objects.get_phds().exists():
            last_grade = Grade.PHD
        elif university_through.objects.get_masters().exists():
            last_grade = Grade.MASTER
        elif university_through.objects.get_bachelors().exists():
            last_grade = Grade.BACHELOR

        self.last_grade = last_grade

    def review_universities(self):
        university_through = UniversityThrough.objects.filter(
            student_detailed_info=self.student_detailed_form
        )

        self._set_grade()
        # User has no previous university!
        if self.last_grade is None:
            return NONE_UNIVERSITY_COMMENT

        # User has previous university
        last_grade_university = university_through.objects.filter(grade=self.last_grade)

        data = {

        }
        #TODO: PHD remained
        if last_grade_university == Grade.MASTER:
            if last_grade_university.university.rank < 850:




    def review_student_detailed_form(self, form):
        data = {
            "age": {
                "title": "سن",
                "message": self._review_age(form.age)
            }
        }
