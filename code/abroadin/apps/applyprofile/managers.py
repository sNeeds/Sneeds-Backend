from django.db import models
from django.db.models import When, Value, Q, Case, IntegerField


class AdmissionQuerySet(models.QuerySet):
    def order_by_grade(self):
        """
            Returns from lower to higher grade. e.g, Bachelor, Master, ...
        """
        from abroadin.apps.data.applydata.models import GradeChoices

        when_list = []

        for grade in GradeChoices.get_ordered():
            q = Q(grade__name=grade)
            when = When(q, then=Value(GradeChoices.order_num(grade)))

            when_list.append(when)

        qs = self.annotate(
            grade_ordering=Case(*when_list, output_field=IntegerField())
        ).order_by('grade_ordering')

        return qs

    def order_by_grade_and_des_rank(self):
        """
        Returns from lower to higher grade and in each part with same grade, it is ordered by destination
        """
        from abroadin.apps.data.applydata.models import GradeChoices
        des_ordered = self.order_by('-destination__rank')
        when_list = []
        counter = 1
        for grade in GradeChoices.get_ordered():
            for obj in des_ordered:
                if obj.grade.name == grade:
                    when_list.append(When(Q(id=obj.id), then=Value(counter)))
                    counter += 1
        qs = self.annotate(
            custom_ordering=Case(*when_list, output_field=IntegerField())
        ).order_by('-custom_ordering')

        return qs
