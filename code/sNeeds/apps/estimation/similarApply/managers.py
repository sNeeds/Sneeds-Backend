from django.db import models


class AppliedStudentDetailedInfoQuerySetManager(models.QuerySet):

    def same_origin_universities(self, universities_qs):
        universities = [u.id for u in universities_qs]
        return self.filter(universities__in=universities)

    def applied_to_universities(self, universities_qs):
        qs = self.none()

        for obj in self._chain():
            if obj.applied_to_has_these_universities(universities_qs):
                qs |= self.filter(id=obj.id)

        return qs

    def same_previous_major(self, major_qs):
        qs = self.none()

        for obj in self._chain():
            if obj.university_through_has_these_majors(major_qs):
                qs |= self.filter(id=obj.id)

        return qs

    def same_applied_to_major(self, major_qs):
        qs = self.none()

        for obj in self._chain():
            if obj.applied_to_has_these_majors(major_qs):
                qs |= self.filter(id=obj.id)

        return qs
