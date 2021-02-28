from django.contrib.contenttypes.models import ContentType

from abroadin.apps.estimation.form.models import WantToApply
from abroadin.apps.applyprofile.models import Admission, ApplyProfile
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
            grade=self.bachelor_grade.name,
            major=self.major1,
            graduate_in=2016,
            gpa=17
        )
        self.form_ed_2 = Education.objects.create(
            content_type=form_ct,
            object_id=self.form_1.id,
            university=self.university1,
            grade=self.master_grade.name,
            major=self.major1,
            graduate_in=2020,
            gpa=18
        )
        self.wta = WantToApply.objects.create(student_detailed_info=self.form_1)
        self.wta.majors.add(self.major1)
        self.wta.grades.add(self.phd_grade)
        self.wta.semester_years.add(self.semester_year1)

        self.profile_ed_1 = Education.objects.create(
            content_type=profile_ct,
            object_id=self.profile_1.id,
            university=self.university1,
            grade=self.bachelor_grade.name,
            major=self.major1,
            graduate_in=2016,
            gpa=17
        )
        self.profile_ed_2 = Education.objects.create(
            content_type=profile_ct,
            object_id=self.profile_1.id,
            university=self.university1,
            grade=self.master_grade.name,
            major=self.major1,
            graduate_in=2020,
            gpa=18
        )
        self.profile_admission_1 = Admission.objects.create(
            apply_profile=self.profile_1,
            major=self.major1,
            grade=self.phd_grade,
            destination=self.university2,
            accepted=True,
            scholarship=20000,
            enroll_year=2021,
        )

        self.class_instance = SimilarProfilesForForm(self.form_1)

    def test__extract_form_majors(self):
        def check_majors_qs_same(majors, majors_list):
            qs = Major.objects.filter(id__in=[major.id for major in majors_list])
            self.assertQuerysetEqual(majors, qs, transform=lambda x: x, ordered=False)

        func = self.class_instance._extract_form_majors
        result = func()
        check_majors_qs_same(result, [self.major1])

        self.form_ed_1.major = self.major2
        self.form_ed_1.save()
        result = func()
        check_majors_qs_same(result, [self.major1, self.major2])

        self.wta.majors.add(self.major3)
        result = func()
        check_majors_qs_same(result, [self.major1, self.major2, self.major3])

    def test__get_related_majors(self):
        func = self.class_instance._get_related_majors

        # The hierarchy
        # m -> mb1 -> mb1b1  -> mb1b1b1 -> mb1b1b1b1
        #                                     -> mb1b1b2 -> mb1b1b2b1
        #                   -> mb1b2 -> mb1b2b1 -> mb1b2b1b1
        #                                      -> mb1b2b2
        #        -> mb2 -> mb2b1  -> mb2b1b1

        m = Major.objects.create(name="m")
        mb1 = Major.objects.create(name="mb1", parent=m)
        mb1b1 = Major.objects.create(name="mb1b1", parent=mb1)
        mb1b1b1 = Major.objects.create(name="mb1b1b1", parent=mb1b1)
        mb1b1b1b1 = Major.objects.create(name="mb1b1b1b1", parent=mb1b1b1)
        mb1b1b2 = Major.objects.create(name="mb1b1b2", parent=mb1b1)
        mb1b1b2b1 = Major.objects.create(name="mb1b1b2b1", parent=mb1b1b2)
        mb1b2 = Major.objects.create(name="mb1b2", parent=mb1)
        mb1b2b1 = Major.objects.create(name="mb1b2b1", parent=mb1b2)
        mb1b2b2 = Major.objects.create(name="mb1b2b2", parent=mb1b2)
        mb2 = Major.objects.create(name="mb2", parent=m)
        mb2b1 = Major.objects.create(name="mb2b1", parent=mb2)
        mb2b1b1 = Major.objects.create(name="mb2b1b1", parent=mb2b1)

        majors = Major.objects.none()
        result = func(majors)
        self.assertQuerysetEqual(result, Major.objects.none(), transform=lambda x: x, ordered=False)

        majors = Major.objects.filter(id=mb1b1b1b1.id)
        result = func(majors)
        self.assertSetEqual(
            set(result),
            {mb1b1, mb1b1b1, mb1b1b2, mb1b1b1b1, mb1b1b2, mb1b1b2b1}
        )

        majors = Major.objects.filter(id__in=[mb1b1b1b1.id, mb2b1.id])
        result = func(majors)
        self.assertSetEqual(
            set(result),
            {mb1b1, mb1b1b1, mb1b1b2, mb1b1b1b1, mb1b1b2, mb1b1b2b1, mb2b1, mb2b1b1}
        )

        majors = Major.objects.filter(id__in=[mb1b1.id])
        result = func(majors)
        self.assertQuerysetEqual(
            result,
            func(Major.objects.filter(id=mb1b1b1b1.id)),
            transform=lambda x: x,
            ordered=False
        )

        majors = Major.objects.filter(id__in=[m.id])
        result = func(majors)
        self.assertSetEqual(
            set(result),
            {m, mb1, mb1b1, mb1b1b1, mb1b1b1b1, mb1b1b2, mb1b1b2b1, mb1b2,
             mb1b2b1, mb1b2b2, mb2, mb2b1, mb2b1b1}
        )

    # def test__similar_profiles_for_data(self):
    #     func = self.class_instance._similar_profiles_for_data
    #
    #     profile = ApplyProfile.objects.create(
    #
    #     )
    #
    # def