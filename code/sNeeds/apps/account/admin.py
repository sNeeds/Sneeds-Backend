from django.contrib import admin

from . import models

admin.site.register(models.University)
admin.site.register(models.FieldOfStudy)
admin.site.register(models.Country)
admin.site.register(models.FieldOfStudyType)
admin.site.register(models.PublicationWhichAuthor)
admin.site.register(models.MaritalStatus)
admin.site.register(models.PaymentAffordability)
admin.site.register(models.Publication)
admin.site.register(models.PublicationType)
admin.site.register(models.LanguageCertificateType)
admin.site.register(models.GRECertificate)
admin.site.register(models.GMATCertificate)


class UniversityThroughInline(admin.TabularInline):
    model = models.UniversityThrough
    extra = 1


class LanguageCertificateTypeThroughInline(admin.TabularInline):
    model = models.LanguageCertificateTypeThrough
    extra = 1


class WantToApplyInline(admin.TabularInline):
    model = models.WantToApply
    extra = 1


class PublicationInline(admin.TabularInline):
    model = models.Publication
    extra = 1


@admin.register(models.StudentDetailedInfo)
class StudentDetailedInfoAdmin(admin.ModelAdmin):
    inlines = [
        UniversityThroughInline,
        LanguageCertificateTypeThroughInline,
        WantToApplyInline,
        PublicationInline,
    ]
    list_display = ['id', 'user']


@admin.register(models.FormGrade)
class StudentDetailedInfoAdmin(admin.ModelAdmin):
    exclude = ['name_search']
