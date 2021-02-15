from datetime import datetime

from rangefilter.filter import DateTimeRangeFilter

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from abroadin.apps.data.applydata import models as ad_models
from abroadin.utils.custom.admin.actions import export_as_csv_action
from abroadin.apps.estimation.similarprofiles.functions import SimilarProfilesForForm

from . import models

LanguageCertificateType = ad_models.LanguageCertificate.LanguageCertificateType


class EducationInline(GenericTabularInline):
    model = ad_models.Education
    autocomplete_fields = ('university', 'major')
    extra = 1


class RegularLanguageCertificateInline(GenericTabularInline):
    model = ad_models.RegularLanguageCertificate
    extra = 1


class GMATCertificateInline(GenericTabularInline):
    model = ad_models.GMATCertificate
    extra = 1


class GREGeneralCertificateInline(GenericTabularInline):
    model = ad_models.GREGeneralCertificate
    extra = 1


class GRESubjectCertificateInline(GenericTabularInline):
    model = ad_models.GRESubjectCertificate
    extra = 1

    def get_queryset(self, request):
        queryset = self.model.objects.filter(
            certificate_type__in=[LanguageCertificateType.GRE_CHEMISTRY,
                                  LanguageCertificateType.GRE_LITERATURE,
                                  LanguageCertificateType.GRE_MATHEMATICS]
        )
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        return queryset


class GREBiologyCertificateInline(GenericTabularInline):
    model = ad_models.GREBiologyCertificate
    extra = 1


class GREPhysicsCertificateInline(GenericTabularInline):
    model = ad_models.GREPhysicsCertificate
    extra = 1


class GREPsychologyCertificateInline(GenericTabularInline):
    model = ad_models.GREPsychologyCertificate
    extra = 1


class DuolingoCertificateInline(GenericTabularInline):
    model = ad_models.DuolingoCertificate
    extra = 1


class PublicationInline(GenericTabularInline):
    model = ad_models.Publication
    extra = 1


class WantToApplyInline(admin.TabularInline):
    model = models.WantToApply
    extra = 1
    filter_horizontal = ['universities']
    autocomplete_fields = ['countries', 'universities', 'majors']


class StudentDetailedInfoBaseAdmin(admin.ModelAdmin):
    inlines = [
        EducationInline,
        PublicationInline,

        RegularLanguageCertificateInline,
        GMATCertificateInline,
        GREGeneralCertificateInline,
        GRESubjectCertificateInline,
        GREBiologyCertificateInline,
        GREPhysicsCertificateInline,
        GREPsychologyCertificateInline,
        DuolingoCertificateInline,
    ]

    list_display = ['id']


@admin.register(models.StudentDetailedInfo)
class StudentDetailedInfoAdmin(StudentDetailedInfoBaseAdmin):
    inlines = [
                  WantToApplyInline
              ] + StudentDetailedInfoBaseAdmin.inlines
    list_filter = (
        ('updated', DateTimeRangeFilter),
        ('created', DateTimeRangeFilter),
    )
    list_display = ['id', 'user', 'value', 'rank', 'updated', 'created', 'is_complete']
    search_fields = ['id', 'user__email']
    actions = [
        export_as_csv_action(
            "Similar Profiles CSV Export",
            fields=['id', 'updated', 'user_id', 'user__email', 'user__phone_number',
                    'last_education__gpa', 'last_education__university__country', 'last_education__university__name',
                    lambda x: [uni.name for uni in x.want_to_apply.universities.all()] if x.is_complete else [],
                    lambda x: list(x.want_to_apply.universities.all().values_list('country__name', flat=True)) if x.get_want_to_apply_or_none() else [],
                    lambda x: [(a.id, a.enroll_year, a.scholarship) for a in SimilarProfilesForForm(x).find_similar_admissions_if_complete()],
                    ],
            file_name='Forms_Similar_Profiles_' + str(datetime.now()),
        )
    ]

    def is_complete(self, instance):
        return instance.is_complete

    is_complete.boolean = True
