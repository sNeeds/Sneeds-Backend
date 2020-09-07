from django.db import models

from sNeeds.apps.account.models import FieldOfStudy, UniversityThrough


class AppliedStudentDetailedInfoQuerySetManager(models.QuerySet):

    def same_origin_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)

    def applied_to_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)

    def same_previous_major(self, major_qs):
        qs = self.none()

        for obj in self._chain():
            if obj.university_through_has_these_majors(major_qs):
                qs |= self.filter(id=obj.id)

        return qs

    def same_applied_to_major(self, major_qs):
        from sNeeds.apps.similarApply.models import AppliedTo
        major_ids = [m.id for m in major_qs]

        related_majors_set = {}

        for obj in self._chain():
            related_majors_set += AppliedTo.objects.filter(
                student_detailed_info=obj,
                major__in=major_ids
            ).major

        related_majors_id_list = [m.id for m in related_majors_set]
        return FieldOfStudy.objects.filter(id__in=related_majors_id_list)
