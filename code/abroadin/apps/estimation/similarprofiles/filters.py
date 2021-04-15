# class SameMajorFilter:
#
#     def filter(self, profiles, ):
from django.db.models import Q

from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.similarprofiles.constraints import SIMILAR_GPA_OFFSET, SIMILAR_UNIVERSITY_RANK_OFFSET


class Filter:
    def get_query(self, profiles, sdi: StudentDetailedInfo) -> Q:
        raise NotImplementedError

    def filter(self, profiles, sdi: StudentDetailedInfo):
        return profiles.filter(self.get_query(profiles, sdi))

    # def get_filter_descriptor(self, sdi):


class SimilarAndWorseGPAFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        offset = SIMILAR_GPA_OFFSET
        assert 0 < offset
        assert offset < 20

        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        gpa = sdi_last_education.gpa

        high_q = Q(educations__gpa__lte=min(20, gpa + offset))
        low_q = Q(educations__gpa__gte=max(0, gpa - offset - 1))
        return high_q


class ExactHomeCountryFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception
        print(sdi_last_education.university.country, sdi_last_education.university.country.id)
        return Q(educations__university__country__id=sdi_last_education.university.country.id)


class ExactHomeUniversityFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception
        return Q(educations__university=sdi_last_education.university)


class SimilarAndWorseHomeUniversityFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        offset = SIMILAR_UNIVERSITY_RANK_OFFSET
        assert 0 < offset
        assert offset < 10000

        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        uni_rank = sdi_last_education.university.rank

        high_q = Q(educations__university__rank__lte=min(12000, uni_rank + offset))
        low_q = Q(educations__university__rank__gte=max(1, uni_rank - offset))
        return low_q


class SimilarHomeUniversityFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        offset = SIMILAR_UNIVERSITY_RANK_OFFSET
        assert 0 < offset
        assert offset < 10000

        # sdi_last_education = sdi.educations.last_education()
        sdi_last_education = sdi.last_education
        if not sdi_last_education:
            raise Exception

        uni_rank = sdi_last_education.university.rank

        high_q = Q(educations__university__rank__lte=min(12000, uni_rank + offset + 150))
        low_q = Q(educations__university__rank__gte=max(1, uni_rank - offset))
        return low_q & high_q


class SameDestinationFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        wta_has_uni = sdi.want_to_apply.universities.all().exists()
        if wta_has_uni:
            return Q(admission__destination__id__in=sdi.want_to_apply.universities.all().values_list('id', flat=True))

        return Q(admission__destination__country__id__in=sdi.want_to_apply.countries.all().values_list('id', flat=True))


class ExactDestinationCountryFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo) -> Q:
        a = set(sdi.want_to_apply.countries.all().values_list('id', flat=True))
        if not a:
            a.union(set(sdi.want_to_apply.universities.values_list('country', flat=True)))

        return Q(admission__destination__country__id__in=a)


class ExactDestinationUniversityFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo) -> Q:
        return Q(admission__destination__id__in=sdi.want_to_apply.universities.all().values_list('id', flat=True))


####################################################
# Home Major Filters
####################################################


class ExactHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = sdi.educations.all().values_list('major__id', flat=True)
        return Q(educations__major__id__in=majors_id)


class MoreSimilarHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = sdi.educations.all().values_list('major__id', flat=True)
        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | set(majors_id)

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l)


class GeneralSimilarHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = sdi.educations.all().values_list('major__id', flat=True)
        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | set(majors_id)

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l) | Q(
            educations__major__parent__parent_id__in=l)


class VeryGeneralSimilarHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = sdi.educations.all().values_list('major__id', flat=True)
        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | set(majors_id) | set(parents_parents_id)

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l)


###########################################
# Destination Major Filter
###########################################


class ExactDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = sdi.want_to_apply.majors.all().values_list('id', flat=True)
        return Q(admission__major__id__in=majors_id)


class MoreSimilarDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = sdi.want_to_apply.majors.all().values_list('id', flat=True)
        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | set(majors_id)
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l)


class GeneralSimilarDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = sdi.want_to_apply.majors.all().values_list('id', flat=True)
        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | set(majors_id)
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l) | Q(
            admission__major__parent__parent_id__in=l)


class VeryGeneralSimilarDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = sdi.want_to_apply.majors.all().values_list('id', flat=True)
        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | set(majors_id) | set(parents_parents_id)
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l)
