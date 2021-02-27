
from ..models import WantToApply, StudentDetailedInfo


class StudentDetailedInfoFixturesMixin:
    def setUp(self):
        super().setUp()

        self.student_detailed_info1 = StudentDetailedInfo.objects.create(
            user=self.user1,
            age=20,
            gender=StudentDetailedInfo.GenderChoices.MALE,
            is_married=True,
            payment_affordability=StudentDetailedInfo.PaymentAffordabilityChoices.LOW,
            prefers_full_fund=True,
            prefers_half_fund=True,
            comment="This is a comment.",
            powerful_recommendation=True,
            related_work_experience=8,
            academic_break=1,
        )

        self.education5.content_object = self.student_detailed_info1
        self.education5.save()

        self.publication4.content_object = self.student_detailed_info1
        self.publication4.save()

        self.publication5.content_object = self.student_detailed_info1
        self.publication5.save()

        self.ielts4.content_object = self.student_detailed_info1
        self.ielts4.save()

        self.gre2.content_object = self.student_detailed_info1
        self.gre2.save()

        #########################################################################

        self.student_detailed_info2 = StudentDetailedInfo.objects.create(
            user=self.user2,
            age=23,
            gender=StudentDetailedInfo.GenderChoices.FEMALE,
            is_married=False,
            payment_affordability=StudentDetailedInfo.PaymentAffordabilityChoices.HIGH,
            prefers_full_fund=True,
            prefers_half_fund=False,
            comment="This is a comment.",
            powerful_recommendation=False,
            related_work_experience=0,
            academic_break=0,
        )

        self.education6.content_object = self.student_detailed_info2
        self.education6.save()

        self.publication6.content_object = self.student_detailed_info2
        self.publication6.save()

        self.ielts5.content_object = self.student_detailed_info2
        self.ielts5.save()

        self.toefl1.content_object = self.student_detailed_info2
        self.toefl1.save()


class WantToApplyFixturesMixin:
    
    def setUp(self):
        super().setUp()
        
        self.want_to_apply1 = WantToApply.objects.create(student_detailed_info=self.student_detailed_info1)
        self.want_to_apply1.majors.add(self.major1)
        self.want_to_apply1.grades.add(self.phd_grade)
        self.want_to_apply1.semester_years.add(self.semester_year1)
        self.want_to_apply1.countries.add(self.country1, self.country2)

        self.want_to_apply2 = WantToApply.objects.create(student_detailed_info=self.student_detailed_info2)
        self.want_to_apply2.majors.add(self.major1, self.major2)
        self.want_to_apply2.grades.add(self.phd_grade)
        self.want_to_apply2.semester_years.add(self.semester_year1, self.semester_year2)
        self.want_to_apply2.countries.add(self.country1, self.country2)
