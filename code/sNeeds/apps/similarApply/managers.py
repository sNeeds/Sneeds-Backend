from django.db import models

from sNeeds.apps.account.models import FieldOfStudy


class AppliedStudentDetailedInfoQuerySetManager(models.QuerySet):
    def same_origin_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)

    def applied_to_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)

    def same_previous_major(self, major_qs):
        majors = [m.id for m in major_qs]
        return self.filter(universities__major__in=majors)

    def same_applied_to_major(self, major_qs):
        from sNeeds.apps.similarApply.models import AppliedTo

        related_majors_set = {}

        for obj in self._chain():
            related_majors_set += AppliedTo.objects.filter(
                student_detailed_info=obj
            ).major

        related_majors_id_list = [m.id for m in related_majors_set]
        return FieldOfStudy.objects.filter(id__in=related_majors_id_list)
