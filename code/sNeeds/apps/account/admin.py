from django.contrib import admin

from . import models

admin.site.register(models.University)
admin.site.register(models.FieldOfStudy)
admin.site.register(models.Country)
admin.site.register(models.FormUniversity)
admin.site.register(models.FormGrade)



class FormUniversityThroughInline(admin.TabularInline):
    model = models.FormUniversityThrough
    extra = 1


@admin.register(models.StudentDetailedInfo)
class StudentDetailedInfoAdmin(admin.ModelAdmin):
    inlines = [FormUniversityThroughInline, ]
    list_display = ['id', 'user']


@admin.register(models.StudentFormFieldsChoice)
class StudentFormFieldsChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category',)
    list_filter = ('category',)
