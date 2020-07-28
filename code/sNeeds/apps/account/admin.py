from django.contrib import admin

from . import models

admin.site.register(models.Country)
admin.site.register(models.UniversityThrough)
admin.site.register(models.FieldOfStudyType)
admin.site.register(models.Publication)
admin.site.register(models.WantToApply)
# admin.site.register(models.GRECertificate)
# admin.site.register(models.GMATCertificate)


class UniversityThroughInline(admin.TabularInline):
    model = models.UniversityThrough
    extra = 1


# class LanguageCertificateTypeInline(admin.TabularInline):
#     model = models.LanguageCertificate
#     extra = 1


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
        # LanguageCertificateTypeInline,
        WantToApplyInline,
        PublicationInline,
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
