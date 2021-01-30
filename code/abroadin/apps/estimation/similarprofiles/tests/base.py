from django.contrib.contenttypes.models import ContentType

from abroadin.apps.applyprofile.models import ApplyProfile
from abroadin.apps.data.account.models import Country, University
from abroadin.apps.data.applydata.models import Grade, Education

from ...form.models import StudentDetailedInfo, WantToApply
from ...tests.base import EstimationBaseTest


class SimilarProfilesBaseTests(EstimationBaseTest):
    def setUp(self):
        super().setUp()

        sdi_content_type = ContentType.objects.get(app_label="form", model='studentdetailedinfo')

        self.form_1 = StudentDetailedInfo.objects.create(
            user=self.user1,
            age=20,
            gender=StudentDetailedInfo.GenderChoices.MALE,
            related_work_experience=0,
            academic_break=0,
            powerful_recommendation=False
        )

        want_to_apply = WantToApply.objects.create(student_detailed_info=self.form_1)
        want_to_apply.countries.add(self.country1)
        want_to_apply.universities.add(self.university1)
        want_to_apply.grades.add(self.grade1)
        want_to_apply.majors.add(self.major1)
        want_to_apply.semester_years.add(self.semester_year1)

        education = Education.objects.create(
            gpa=18,
            content_type=sdi_content_type,
            object_id=self.form_1.id,
            major=self.major2,
            university=self.university2,
            graduate_in=2020
        )

        self.apply_profile_1 = ApplyProfile.objects.create(
            name="profile 1",
            gap=5,
        )
