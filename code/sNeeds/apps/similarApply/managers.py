from django.db import models


class AppliedStudentDetailedInfoQuerySetManager(models.QuerySet):
    def same_origin_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)

    def applied_to_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)
