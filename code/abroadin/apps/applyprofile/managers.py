from django.db import models
from django.db.models import When, Value, Q, Case, IntegerField


class AdmissionQuerySet(models.QuerySet):
    def order_by_grade(self):
        """
            Returns from lower to higher grade. e.g, Bachelor, Master, ...
        """
        from .models import GradeChoices

        when_list = []

        for grade in GradeChoices.get_ordered():
            q = Q(grade__name=grade)
            when = When(q, then=Value(GradeChoices.order_num(grade)))

            when_list.append(when)

        qs = self.annotate(
            grade_ordering=Case(*when_list, output_field=IntegerField())
        ).order_by('grade_ordering')

        return qs
