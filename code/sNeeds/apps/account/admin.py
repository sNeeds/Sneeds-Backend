from django.contrib import admin

from . import models

admin.site.register(models.Country)
admin.site.register(models.UniversityThrough)
admin.site.register(models.FieldOfStudyType)
admin.site.register(models.Publication)
admin.site.register(models.WantToApply)


class UniversityThroughInline(admin.TabularInline):
    model = models.UniversityThrough
    extra = 1


class RegularLanguageCertificateTypeInline(admin.TabularInline):
    model = models.RegularLanguageCertificate
    extra = 1


class GMATCertificateTypeInline(admin.TabularInline):
    model = models.GMATCertificate
    extra = 1


class GREGeneralCertificateTypeInline(admin.TabularInline):
    model = models.GREGeneralCertificate
    extra = 1


class GRESubjectCertificateTypeInline(admin.TabularInline):
    model = models.GRESubjectCertificate
    extra = 1


class GREBiologyCertificateTypeInline(admin.TabularInline):
    model = models.GREBiologyCertificate
    extra = 1


class GREPhysicsCertificateTypeInline(admin.TabularInline):
    model = models.GREPhysicsCertificate
    extra = 1


class GREPsychologyCertificate(admin.TabularInline):
    model = models.GREPsychologyCertificate
    extra = 1


class DuolingoCertificateCertificate(admin.TabularInline):
    model = models.DuolingoCertificate
    extra = 1


class WantToApplyInline(admin.TabularInline):
    model = models.WantToApply
    extra = 1
    filter_horizontal = ['universities']


class PublicationInline(admin.TabularInline):
    model = models.Publication
    extra = 1


@admin.register(models.StudentDetailedInfo)
class StudentDetailedInfoAdmin(admin.ModelAdmin):
    inlines = [
        UniversityThroughInline,
        WantToApplyInline,
        PublicationInline,

        RegularLanguageCertificateTypeInline,
        GMATCertificateTypeInline,
        GREGeneralCertificateTypeInline,
        GRESubjectCertificateTypeInline,
        GREBiologyCertificateTypeInline,
        GREPhysicsCertificateTypeInline,
        GREPsychologyCertificate,
        DuolingoCertificateCertificate,
    ]

    list_display = ['id', 'user', 'age', 'is_married']


@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rank', 'is_college']
    search_fields = ['name']


@admin.register(models.FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'major_type']
    search_fields = ['name', ]
    list_filter = ['major_type']
