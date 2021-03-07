import decimal

from django.db.models import When, Value, Q, Case, BooleanField

from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.similarprofiles.constraints import SIMILAR_GPA_OFFSET, EXACT_GPA_OFFSET


class SimilarGPA:
    title = 'Similar GPA'
    annotation_field = 'similar_gpa'

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        # queryset = ApplyProfile.objects.all()
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        gpa = sdi_last_education.gpa

        gpa_low = max(0, gpa - SIMILAR_GPA_OFFSET)
        gpa_high = min(20, gpa + SIMILAR_GPA_OFFSET)
        high_q = Q(educations__gpa__lte=gpa_high)
        low_q = Q(educations__gpa__gte=gpa_low)

        annotation_dict = {
            self.annotation_field: Case((When(high_q & low_q, then=Value(True))),
                                        default=Value(False), output_field=BooleanField())
        }
        qs = queryset.annotate(**annotation_dict)
        return qs

    def tag_object(self, obj, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        gpa = sdi_last_education.gpa
        gpa_low = max(0, gpa - SIMILAR_GPA_OFFSET)
        gpa_high = min(20, gpa + SIMILAR_GPA_OFFSET)
        if obj.educations.filter(gpa__lte=gpa_high, gpa__gte=gpa_low).exists():
            setattr(obj, self.annotation_field, True)
        else:
            setattr(obj, self.annotation_field, False)
        return obj


class ExactGPA:
    title = 'Exact GPA'
    annotation_field = 'exact_gpa'

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        gpa = sdi_last_education.gpa

        gpa_low = max(0, gpa - decimal.Decimal(EXACT_GPA_OFFSET))
        gpa_high = min(20, gpa + decimal.Decimal(EXACT_GPA_OFFSET))
        high_q = Q(educations__gpa__lte=gpa_high)
        low_q = Q(educations__gpa__gte=gpa_low)

        annotation_dict = {
            self.annotation_field: Case((When(high_q & low_q, then=Value(True))),
                                        default=Value(False), output_field=BooleanField())
        }
        qs = queryset.annotate(**annotation_dict)
        return qs

    def tag_object(self, obj, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        gpa = sdi_last_education.gpa
        gpa_low = max(0, gpa - decimal.Decimal(EXACT_GPA_OFFSET))
        gpa_high = min(20, gpa + decimal.Decimal(EXACT_GPA_OFFSET))

        if obj.educations.filter(gpa__lte=gpa_high, gpa__gte=gpa_low).exists():
            setattr(obj, self.annotation_field, True)
        else:
            setattr(obj, self.annotation_field, False)
        return obj
