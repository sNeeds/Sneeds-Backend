from django.db import models


class AppliedStudentDetailedInfoManager(models.QuerySet):
    def get_applied_to_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)

    def get_applied_to_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)
