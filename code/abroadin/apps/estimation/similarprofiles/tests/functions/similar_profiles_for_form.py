from django.contrib.contenttypes.models import ContentType

from abroadin.apps.estimation.form.models import WantToApply
from abroadin.apps.applyprofile.models import Admission
from abroadin.apps.data.applydata.models import Education
from abroadin.apps.data.account.models import Major

from .base import SimilarProfilesFunctionsBaseTests
from ...functions import SimilarProfilesForForm


class SimilarProfilesForFormTests(SimilarProfilesFunctionsBaseTests):
    def setUp(self):
        super().setUp()

        form_ct = ContentType.objects.get(app_label='form', model='studentdetailedinfo')
        profile_ct = ContentType.objects.get(app_label='applyprofile', model='applyprofile')

        self.form_ed_1 = Education.objects.create(
            content_type=form_ct,
            object_id=self.form_1.id,
            university=self.university1,
            grade=self.grade_bachelor.name,
            major=self.major1,
            graduate_in=2016,
            gpa=17
        )
        self.form_ed_2 = Education.objects.create(
            content_type=form_ct,
            object_id=self.form_1.id,
            university=self.university1,
            grade=self.grade_master.name,
            major=self.major1,
            graduate_in=2020,
            gpa=18
        )
        self.wta = WantToApply.objects.create(student_detailed_info=self.form_1)
        self.wta.majors.add(self.major1)
        self.wta.grades.add(self.grade_phd)
        self.wta.semester_years.add(self.semester_year1)

        self.profile_ed_1 = Education.objects.create(
            content_type=profile_ct,
            object_id=self.profile_1.id,
            university=self.university1,
            grade=self.grade_bachelor.name,
            major=self.major1,
            graduate_in=2016,
            gpa=17
        )
        self.profile_ed_2 = Education.objects.create(
            content_type=profile_ct,
            object_id=self.profile_1.id,
            university=self.university1,
            grade=self.grade_master.name,
            major=self.major1,
            graduate_in=2020,
            gpa=18
        )
        self.profile_admission_1 = Admission.objects.create(
            apply_profile=self.profile_1,
            major=self.major1,
            grade=self.grade_phd,
            destination=self.university2,
            accepted=True,
            scholarship=20000,
            enroll_year=2021,
        )

        self.class_instance = SimilarProfilesForForm(self.form_1)

    def test__extract_form_data_majors(self):
        def check_majors_qs_same(majors, majors_list):
            qs = Major.objects.filter(id__in=[major.id for major in majors_list])
            self.assertQuerysetEqual(majors, qs, transform=lambda x: x, ordered=False)

        func = self.class_instance._extract_related_majors
        result = func()
        check_majors_qs_same(result, [self.major1])

        self.form_ed_1.major = self.major2
        self.form_ed_1.save()
        result = func()
        check_majors_qs_same(result, [self.major1, self.major2])

        self.wta.majors.add(self.major3)
        result = func()
        check_majors_qs_same(result, [self.major1, self.major2, self.major3])

