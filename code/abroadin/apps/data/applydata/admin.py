from datetime import datetime

from django.contrib import admin

from abroadin.utils.custom.admin.actions import export_as_csv_action
from . import models

admin.site.register(models.Grade)
admin.site.register(models.SemesterYear)


@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    actions = [
        export_as_csv_action(
            "CSV Export",
            fields=['id', 'content_type', 'object_id', 'gpa', 'graduate_in',
                    'major', 'grade', 'university__name',
                    ],
            file_name='Educations_' + str(datetime.now()),
        )]


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'value']
    readonly_fields = ['value']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


@admin.register(models.LanguageCertificate)
class LanguageCertificateAdmin(admin.ModelAdmin):
    list_display = ['id', 'certificate_type', 'real_type']
    readonly_fields = ['real_type']


@admin.register(models.RegularLanguageCertificate)
class RegularLanguageCertificateAdmin(LanguageCertificateAdmin):
    readonly_fields = ['real_type']


@admin.register(models.GMATCertificate)
class GMATCertificateAdmin(LanguageCertificateAdmin):
    pass


@admin.register(models.GREGeneralCertificate)
class GREGeneralCertificateAdmin(LanguageCertificateAdmin):
    pass


@admin.register(models.GRESubjectCertificate)
class GRESubjectCertificateAdmin(LanguageCertificateAdmin):
    pass


@admin.register(models.GREPsychologyCertificate)
class GREPsychologyCertificateAdmin(LanguageCertificateAdmin):
    pass


@admin.register(models.GREPhysicsCertificate)
class GREPhysicsCertificateAdmin(LanguageCertificateAdmin):
    pass


@admin.register(models.GREBiologyCertificate)
class GREBiologyCertificateAdmin(LanguageCertificateAdmin):
    pass


@admin.register(models.DuolingoCertificate)
class DuolingoCertificateAdmin(LanguageCertificateAdmin):
    pass
