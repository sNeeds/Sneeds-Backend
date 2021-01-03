from django.contrib import admin

from . import models

admin.site.register(models.Grade)
admin.site.register(models.SemesterYear)
admin.site.register(models.Education)
admin.site.register(models.RegularLanguageCertificate)
admin.site.register(models.GMATCertificate)
admin.site.register(models.DuolingoCertificate)
admin.site.register(models.GREGeneralCertificate)
admin.site.register(models.GRESubjectCertificate)
admin.site.register(models.GREPsychologyCertificate)
admin.site.register(models.GREPhysicsCertificate)
admin.site.register(models.GREBiologyCertificate)


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'value']
    readonly_fields = ['value']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
