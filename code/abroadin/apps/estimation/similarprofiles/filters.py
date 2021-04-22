from django.db.models import Q

from abroadin.apps.data.globaldata.models import Major
from abroadin.apps.estimation.form.exceptions import SDIEducationLeakage
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.similarprofiles.constraints import SIMILAR_GPA_OFFSET, SIMILAR_UNIVERSITY_RANK_OFFSET
from abroadin.apps.estimation.form import exceptions as sdi_exception


class Filter:
    raise_defect_exception = None
    accepted_defect_exceptions = None

    def __init__(self, **kwargs):
        self.raise_defect_exception = kwargs.pop('raise_defect_exception', False)
        self.accepted_defect_exceptions = kwargs.pop('accepted_defect_exceptions', [])

    def get_query(self, profiles, sdi: StudentDetailedInfo) -> Q:
        raise NotImplementedError

    def filter(self, profiles, sdi: StudentDetailedInfo):
        return profiles.filter(self.get_query(profiles, sdi))


class SimilarAndWorseGPAFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        offset = SIMILAR_GPA_OFFSET
        assert 0 < offset
        assert offset < 20

        sdi_last_education = sdi.last_education
        if sdi_last_education is None:
            if self.raise_defect_exception and SDIEducationLeakage in self.accepted_defect_exceptions:
                raise SDIEducationLeakage()
            return Q(pk__in=[])

        gpa = sdi_last_education.gpa

        high_q = Q(educations__gpa__lte=min(20, gpa + offset))
        low_q = Q(educations__gpa__gte=max(0, gpa - offset - 1))
        return high_q


class ExactHomeCountryFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        sdi_last_education = sdi.last_education
        if sdi_last_education is None:
            if self.raise_defect_exception and SDIEducationLeakage in self.accepted_defect_exceptions:
                raise SDIEducationLeakage()
            return Q(pk__in=[])
        # print(sdi_last_education.university.country, sdi_last_education.university.country.id)
        return Q(educations__university__country__id=sdi_last_education.university.country.id)


class ExactHomeUniversityFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):

        sdi_last_education = sdi.last_education
        if sdi_last_education is None:
            if self.raise_defect_exception and SDIEducationLeakage in self.accepted_defect_exceptions:
                raise SDIEducationLeakage()
            return Q(pk__in=[])

        return Q(educations__university=sdi_last_education.university)


class SimilarAndWorseHomeUniversityFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):

        sdi_last_education = sdi.last_education
        if sdi_last_education is None:
            if self.raise_defect_exception and SDIEducationLeakage in self.accepted_defect_exceptions:
                raise SDIEducationLeakage()
            return Q(pk__in=[])

        offset = SIMILAR_UNIVERSITY_RANK_OFFSET
        assert 0 < offset
        assert offset < 10000

        uni_rank = sdi_last_education.university.rank

        high_q = Q(educations__university__rank__lte=min(12000, uni_rank + offset))
        low_q = Q(educations__university__rank__gte=max(1, uni_rank - offset))
        return low_q


class SimilarHomeUniversityFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):

        sdi_last_education = sdi.last_education
        if sdi_last_education is None:
            if self.raise_defect_exception and SDIEducationLeakage in self.accepted_defect_exceptions:
                raise SDIEducationLeakage()
            return Q(pk__in=[])

        offset = SIMILAR_UNIVERSITY_RANK_OFFSET
        assert 0 < offset
        assert offset < 10000

        sdi_last_education = sdi.last_education
        if sdi_last_education is None:
            if self.raise_defect_exception and SDIEducationLeakage in self.accepted_defect_exceptions:
                raise SDIEducationLeakage()
            return Q(pk__in=[])

        uni_rank = sdi_last_education.university.rank

        high_q = Q(educations__university__rank__lte=min(12000, uni_rank + offset + 150))
        low_q = Q(educations__university__rank__gte=max(1, uni_rank - offset))
        return low_q & high_q


class SameDestinationFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        wta_unis = set(sdi.want_to_apply.universities.all().values_list('id', flat=True))
        wta_countries = set(sdi.want_to_apply.countries.all().values_list('id', flat=True))
        if wta_unis:
            return Q(admission__destination__id__in=wta_unis)
        if wta_countries:
            return Q(admission__destination__country__id__in=wta_countries)
        if self.raise_defect_exception and \
                sdi_exception.SDIWantToApplyUniversityAndCountryLeakage in self.accepted_defect_exceptions:
            raise sdi_exception.SDIWantToApplyUniversityAndCountryLeakage()
        return Q(pk__in=[])


class ExactDestinationCountryFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo) -> Q:
        a = set(sdi.want_to_apply.countries.all().values_list('id', flat=True))
        if not a:
            a.union(set(sdi.want_to_apply.universities.values_list('country', flat=True)))

        return Q(admission__destination__country__id__in=a)


class ExactDestinationUniversityFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo) -> Q:
        wta_unis = set(sdi.want_to_apply.universities.all().values_list('id', flat=True))
        if not wta_unis and self.raise_defect_exception \
                and sdi_exception.SDIWantToApplyUniversityLeakage in self.accepted_defect_exceptions:
            raise sdi_exception.SDIWantToApplyUniversityLeakage()
        return Q(admission__destination__id__in=wta_unis)


####################################################
# Home Major Filters
####################################################


class ExactHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.educations.all().values_list('major__id', flat=True))
        return Q(educations__major__id__in=majors_id)


class VerySimilarHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.educations.all().values_list('major__id', flat=True))
        if not majors_id:
            print('Not majors id')
            if self.raise_defect_exception \
                    and sdi_exception.SDIEducationLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIEducationLeakage()
            return Q(pk__in=[])

        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | majors_id

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l)


class SimilarHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.educations.all().values_list('major__id', flat=True))
        if not majors_id:
            print('Not majors id')
            if self.raise_defect_exception \
                    and sdi_exception.SDIEducationLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIEducationLeakage()
            return Q(pk__in=[])

        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent__in=majors_id).values_list('id', flat=True)
        print('child id', list(children_id))
        l = set(parents_id) | majors_id | set(children_id)
        print(l)

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l)


class GeneralSimilarHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.educations.all().values_list('major__id', flat=True))
        if not majors_id:
            print('Not majors id')
            if self.raise_defect_exception \
                    and sdi_exception.SDIEducationLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIEducationLeakage()
            return Q(pk__in=[])

        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent__in=majors_id).values_list('id', flat=True)
        parents_children_id = Major.objects.filter(parent__in=parents_id).values_list('id', flat=True)
        # print('child id', list(children_id))
        l = set(parents_id) | majors_id | set(children_id)
        # print(l)

        return Q(educations__major__id__in=l | set(parents_children_id)) | Q(educations__major__parent_id__in=l)


class MoreGeneralSimilarHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.educations.all().values_list('major__id', flat=True))
        if not majors_id:
            print('Not majors id')
            if self.raise_defect_exception \
                    and sdi_exception.SDIEducationLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIEducationLeakage()
            return Q(pk__in=[])
        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent__in=majors_id).values_list('id', flat=True)
        parents_children_id = Major.objects.filter(parent__in=parents_id).values_list('id', flat=True)
        l = set(parents_id) | majors_id | set(children_id) | set(parents_children_id)

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l) | Q(
            educations__major__parent__parent_id__in=l)


class MoreGeneralSimilarHomeMajorsFilter2(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.educations.all().values_list('major__id', flat=True))
        if not majors_id:
            print('Not majors id')
            if self.raise_defect_exception \
                    and sdi_exception.SDIEducationLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIEducationLeakage()
            return Q(pk__in=[])
        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent__in=majors_id).values_list('id', flat=True)
        parents_children_id = Major.objects.filter(parent__in=parents_id).values_list('id', flat=True)
        l = set(parents_id) | majors_id | set(children_id) | set(parents_children_id)

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l) | Q(
            educations__major__parent__parent_id__in=l)


class VeryGeneralSimilarHomeMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.educations.all().values_list('major__id', flat=True))
        if not majors_id:
            print('Not majors id')
            if self.raise_defect_exception \
                    and sdi_exception.SDIEducationLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIEducationLeakage()
            return Q(pk__in=[])
        parents_id = sdi.educations.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.educations.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | majors_id | set(parents_parents_id)

        return Q(educations__major__id__in=l) | Q(educations__major__parent_id__in=l)


###########################################
# Destination Major Filter
###########################################


class ExactDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.want_to_apply.majors.all().values_list('id', flat=True))
        if not majors_id:
            if self.raise_defect_exception \
                    and sdi_exception.SDIWantToApplyMajorLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIWantToApplyMajorLeakage()
            return Q(pk__in=[])
        return Q(admission__major__id__in=majors_id)


class VerySimilarDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.want_to_apply.majors.all().values_list('id', flat=True))
        if not majors_id:
            if self.raise_defect_exception \
                    and sdi_exception.SDIWantToApplyMajorLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIWantToApplyMajorLeakage()
            return Q(pk__in=[])
        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent=sdi.last_education.major).values_list('id', flat=True)
        l = set(parents_id) | majors_id
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l)


class SimilarDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.want_to_apply.majors.all().values_list('id', flat=True))

        if not majors_id:
            if self.raise_defect_exception \
                    and sdi_exception.SDIWantToApplyMajorLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIWantToApplyMajorLeakage()
            return Q(pk__in=[])

        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent__in=majors_id).values_list('id', flat=True)

        l = set(parents_id) | majors_id | set(children_id)
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l)


class GeneralSimilarDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.want_to_apply.majors.all().values_list('id', flat=True))

        if not majors_id:
            if self.raise_defect_exception \
                    and sdi_exception.SDIWantToApplyMajorLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIWantToApplyMajorLeakage()
            return Q(pk__in=[])

        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent__in=majors_id).values_list('id', flat=True)
        parents_children_id = Major.objects.filter(parent__in=parents_id).values_list('id', flat=True)

        l = set(parents_id) | majors_id | set(children_id)
        return Q(admission__major__id__in=l | set(parents_children_id)) | Q(admission__major__parent_id__in=l)


class MoreGeneralSimilarDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.want_to_apply.majors.all().values_list('id', flat=True))
        if not majors_id:
            if self.raise_defect_exception \
                    and sdi_exception.SDIWantToApplyMajorLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIWantToApplyMajorLeakage()
            return Q(pk__in=[])
        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent__in=majors_id).values_list('id', flat=True)
        parents_children_id = Major.objects.filter(parent__in=parents_id).values_list('id', flat=True)

        l = set(parents_id) | majors_id | set(children_id) | set(parents_children_id)
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l)


class MoreGeneralSimilarDestinationMajorsFilter2(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.want_to_apply.majors.all().values_list('id', flat=True))
        if not majors_id:
            if self.raise_defect_exception \
                    and sdi_exception.SDIWantToApplyMajorLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIWantToApplyMajorLeakage()
            return Q(pk__in=[])
        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        children_id = Major.objects.filter(parent__in=majors_id).values_list('id', flat=True)
        parents_children_id = Major.objects.filter(parent__in=parents_id).values_list('id', flat=True)

        l = set(parents_id) | majors_id | set(children_id) | set(parents_children_id)
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l) | Q(
            admission__major__parent__parent_id__in=l)


class VeryGeneralSimilarDestinationMajorsFilter(Filter):

    def get_query(self, profiles, sdi: StudentDetailedInfo):
        majors_id = set(sdi.want_to_apply.majors.all().values_list('id', flat=True))
        if not majors_id:
            print('Not majors id')
            if self.raise_defect_exception \
                    and sdi_exception.SDIWantToApplyMajorLeakage in self.accepted_defect_exceptions:
                raise sdi_exception.SDIWantToApplyMajorLeakage()
            return Q(pk__in=[])
        parents_id = sdi.want_to_apply.majors.all().values_list('major__parent_id', flat=True)
        parents_parents_id = sdi.want_to_apply.majors.all().values_list('major__parent__parent_id', flat=True)
        l = set(parents_id) | majors_id | set(parents_parents_id)
        return Q(admission__major__id__in=l) | Q(admission__major__parent_id__in=l)
