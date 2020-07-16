from django.contrib import admin

from . import models

admin.site.register(models.University)
admin.site.register(models.FieldOfStudy)
admin.site.register(models.Country)
admin.site.register(models.FormUniversity)
admin.site.register(models.FormGrade)
admin.site.register(models.FormMajor)
admin.site.register(models.FormMajorType)
admin.site.register(models.PublicationWhichAuthor)
admin.site.register(models.PaymentAffordability)
admin.site.register(models.Publication)
admin.site.register(models.PublicationType)
admin.site.register(models.LanguageCertificateType)


class FormUniversityThroughInline(admin.TabularInline):
    model = models.FormUniversityThrough
    extra = 1


class LanguageCertificateTypeThroughInline(admin.TabularInline):
    model = models.LanguageCertificateTypeThrough
    extra = 1


class UniversityWantToApplyThroughInline(admin.TabularInline):
    model = models.UniversityWantToApplyThrough
    extra = 1


@admin.register(models.StudentDetailedInfo)
class StudentDetailedInfoAdmin(admin.ModelAdmin):
    inlines = [
        FormUniversityThroughInline,
        LanguageCertificateTypeThroughInline
    ]
    list_display = ['id', 'user']
    filter_horizontal = ['want_to_apply', 'publications']


@admin.register(models.WantToApply)
class WantToApplyAdmin(admin.ModelAdmin):
    inlines = [UniversityWantToApplyThroughInline]

