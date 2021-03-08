import decimal

from django.db.models import When, Value, Q, Case, BooleanField

from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.similarprofiles.constraints import SIMILAR_GPA_OFFSET, EXACT_GPA_OFFSET


class Tag:
    title = None
    annotation_field = None
    annotation_dict = None

    def get_annotation_dict(self, queryset, sdi: StudentDetailedInfo):
        raise NotImplementedError

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        raise NotImplementedError

    def tag_object(self, obj, sdi: StudentDetailedInfo):
        raise NotImplementedError


class SimilarGPA(Tag):
    title = 'Similar GPA'
    annotation_field = 'similar_gpa'
    annotation_dict = None

    def get_annotation_dict(self, queryset, sdi: StudentDetailedInfo):
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
                                        default=Value(False), output_field=BooleanField()),
            'aaa': Case((When(high_q, then=Value(True))),
                        default=Value(False), output_field=BooleanField()),
        }
        return annotation_dict

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        qs = queryset.annotate(**self.get_annotation_dict(queryset, sdi))
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


class ExactGPA(Tag):
    title = 'Exact GPA'
    annotation_field = 'exact_gpa'
    annotation_dict = None

    def get_annotation_dict(self, queryset, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        gpa = sdi_last_education.gpa

        gpa_low = max(0, gpa - decimal.Decimal(EXACT_GPA_OFFSET))
        gpa_high = min(20, gpa + decimal.Decimal(EXACT_GPA_OFFSET))
        high_q = Q(educations__gpa__lte=gpa_high)
        low_q = Q(educations__gpa__gte=gpa_low)

        return {
            self.annotation_field: Case((When(high_q & low_q, then=Value(True))),
                                        default=Value(False), output_field=BooleanField())
        }

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        qs = queryset.annotate(**self.get_annotation_dict(queryset, sdi))
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


class ExactHomeUniversity(Tag):
    title = 'Exact Home University'
    annotation_field = 'exact_home_university'
    annotation_dict = None

    def get_annotation_dict(self, queryset, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        home_university = sdi_last_education.university

        education_q = Q(educations__university=home_university)

        return {
            self.annotation_field: Case((When(education_q, then=Value(True))),
                                        default=Value(False), output_field=BooleanField())
        }

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        qs = queryset.annotate(**self.get_annotation_dict(queryset, sdi))
        return qs

    def tag_object(self, obj, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        home_university = sdi_last_education.gpa

        if obj.educations.filter(university=home_university).exists():
            setattr(obj, self.annotation_field, True)
        else:
            setattr(obj, self.annotation_field, False)
        return obj


class ExactHomeMajor(Tag):
    title = 'Exact Home Major'
    annotation_field = 'exact_home_major'

    def get_annotation_dict(self, queryset, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        home_major = sdi_last_education.major

        major_q = Q(educations__major=home_major)

        return {
            self.annotation_field: Case((When(major_q, then=Value(True))),
                                        default=Value(False), output_field=BooleanField())
        }

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        qs = queryset.annotate(**self.get_annotation_dict(queryset, sdi))
        return qs

    def tag_object(self, obj, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        home_major = sdi_last_education.gpa

        if obj.educations.filter(major=home_major).exists():
            setattr(obj, self.annotation_field, True)
        else:
            setattr(obj, self.annotation_field, False)
        return obj


class SimilarHomeMajor(Tag):
    title = 'Similar Home Major'
    annotation_field = 'similar_home_major'
    annotation_dict = None

    def get_annotation_dict(self, queryset, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        home_major = sdi_last_education.major

        major_q = Q(educations__major=home_major)

        return {
            self.annotation_field: Case((When(major_q, then=Value(True))),
                                        default=Value(False), output_field=BooleanField())
        }

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        qs = queryset.annotate(**self.get_annotation_dict(queryset, sdi))
        return qs

    def tag_object(self, obj, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.educations.last_education()
        if not sdi_last_education:
            raise Exception

        home_major = sdi_last_education.gpa

        if obj.educations.filter(major=home_major).exists():
            setattr(obj, self.annotation_field, True)
        else:
            setattr(obj, self.annotation_field, False)
        return obj


# majors = self._get_related_majors(form_majors)
