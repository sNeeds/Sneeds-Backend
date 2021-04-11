import decimal

from django.db.models import When, Value, Q, Case, BooleanField, OuterRef, Exists

from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.similarprofiles.constraints import SIMILAR_GPA_OFFSET, EXACT_GPA_OFFSET, \
    SIMILAR_UNIVERSITY_RANK_OFFSET
from abroadin.apps.estimation.similarprofiles.functions import SimilarProfilesForForm


class Tag:
    title = None
    annotation_field = None
    annotation_dict = None
    inner_annotation_field = None

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        raise NotImplementedError

    def get_inner_annotation_dict(self, queryset, sdi: StudentDetailedInfo):
        annotation_dict = {
            self.inner_annotation_field: Case((When(self.get_inner_query(queryset, sdi), then=Value(True))),
                                              default=Value(False), output_field=BooleanField()),
        }
        return annotation_dict

    def get_annotation_dict(self, queryset, sdi: StudentDetailedInfo):
        q = queryset.filter(**{self.inner_annotation_field: True, 'pk': OuterRef('pk')})
        annotation_dict = {
            self.annotation_field: Case((When(Exists(q), then=Value(True))),
                                        default=Value(False), output_field=BooleanField()),
        }
        return annotation_dict

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        qs = queryset.annotate(**self.get_inner_annotation_dict(queryset, sdi))
        qs = qs.annotate(**self.get_annotation_dict(qs, sdi))
        return qs

    def get_tagged_ids_list(self, queryset, sdi: StudentDetailedInfo):
        return queryset.filter(self.get_inner_query(queryset, sdi)).values_list('id', flat=True)

    def tag_queryset2(self, queryset, sdi: StudentDetailedInfo):
        qs = queryset.annotate(**{
            self.annotation_field: Case(
                (When(Q(id__in=self.get_tagged_ids_list(queryset, sdi)), then=Value(True))),
                default=Value(False), output_field=BooleanField()),
        })
        return qs

    def tag_object(self, obj, sdi: StudentDetailedInfo):
        object_queryset = obj.__class__.objects.filter(pk=obj.pk)

        if object_queryset.filter(self.get_inner_query(object_queryset, sdi)).exists():
            setattr(obj, self.annotation_field, True)
        else:
            setattr(obj, self.annotation_field, False)
        # print(obj, getattr(obj, self.annotation_field))
        return obj


class SimilarGPA(Tag):
    title = 'Similar GPA'
    annotation_field = 'similar_gpa'
    inner_annotation_field = 'inner_' + annotation_field
    annotation_dict = None

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        gpa = sdi_last_education.gpa

        gpa_low = max(0, gpa - SIMILAR_GPA_OFFSET)
        gpa_high = min(20, gpa + SIMILAR_GPA_OFFSET)
        high_q = Q(educations__gpa__lte=gpa_high)
        low_q = Q(educations__gpa__gte=gpa_low)

        return high_q & low_q

    # def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
    #     qs = queryset.annotate(**self.get_inner_annotation_dict(queryset, sdi))
    #     # qs = qs.annotate(**self.get_annotation_dict(qs, sdi))
    #     return qs


class ExactGPA(Tag):
    title = 'Exact GPA'
    annotation_field = 'exact_gpa'
    inner_annotation_field = 'inner_' + annotation_field

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        gpa = sdi_last_education.gpa

        gpa_low = max(0, gpa - decimal.Decimal(EXACT_GPA_OFFSET))
        gpa_high = min(20, gpa + decimal.Decimal(EXACT_GPA_OFFSET))
        high_q = Q(educations__gpa__lte=gpa_high)
        low_q = Q(educations__gpa__gte=gpa_low)

        return low_q & high_q

    # def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
    #     qs = queryset.annotate(**self.get_annotation_dict(queryset, sdi))
    #     return qs


class ExactHomeUniversity(Tag):
    title = 'Exact Home University'
    annotation_field = 'exact_home_university'
    inner_annotation_field = 'inner_' + annotation_field

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        home_university = sdi_last_education.university

        return Q(educations__university=home_university)

    # def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
    #     qs = queryset.annotate(**self.get_annotation_dict(queryset, sdi))
    #     return qs


class ExactHomeMajor(Tag):
    title = 'Exact Home Major'
    annotation_field = 'exact_home_major'
    inner_annotation_field = 'inner_' + annotation_field

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        home_major = sdi_last_education.major

        return Q(educations__major=home_major)


class SimilarHomeMajor(Tag):
    title = 'Similar Home Major'
    annotation_field = 'similar_home_major'
    inner_annotation_field = 'inner_' + annotation_field

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        # s = SimilarProfilesForForm(form=sdi)
        # majors = s._get_related_majors(s._extract_form_home_majors(sdi))
        majors_id = sdi.educations.all().values_list('major__id', flat=True)
        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | set(majors_id)

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l)


class ExactDestinationMajor(Tag):
    title = 'Exact Destination Major'
    annotation_field = 'exact_destination_major'
    inner_annotation_field = 'inner_' + annotation_field

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        wta_majors = sdi.want_to_apply.majors.values_list('id', flat=True)
        return Q(educations__major_id__in=wta_majors)


class SimilarDestinationMajor(Tag):
    title = 'Similar Destination Major'
    annotation_field = 'similar_destination_major'
    inner_annotation_field = 'inner_' + annotation_field

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        majors_id = sdi.want_to_apply.majors.all().values_list('id', flat=True)
        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        l = set(parents_id) | set(majors_id)
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l)


class SimilarHomeUniversity(Tag):
    title = 'Similar Home University'
    annotation_field = 'similar_home_university'
    inner_annotation_field = 'inner_' + annotation_field

    def get_inner_query(self, queryset, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        uni_rank, uni_country = sdi_last_education.university.rank, sdi_last_education.university.country

        uni_rank_low = max(1, uni_rank - SIMILAR_UNIVERSITY_RANK_OFFSET)
        uni_rank_high = min(8000, uni_rank + SIMILAR_UNIVERSITY_RANK_OFFSET)
        high_q = Q(educations__university__rank__lte=uni_rank_high)
        low_q = Q(educations__university__rank__gte=uni_rank_low)
        # TODO Provide Similar Countries, for example Iran and Turkey are similar
        country_q = Q(educations__university__country=uni_country)

        return high_q & low_q & country_q

    # def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
    #     qs = queryset.annotate(**self.get_annotation_dict(queryset, sdi))
    #     return qs
