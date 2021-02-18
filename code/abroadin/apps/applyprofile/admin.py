from datetime import datetime

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import ApplyProfile, Admission
from abroadin.apps.data.applydata.models import (
    Publication, Education, RegularLanguageCertificate, GMATCertificate, DuolingoCertificate,
    GRESubjectCertificate, GREGeneralCertificate, GREPsychologyCertificate, GREPhysicsCertificate,
    GREBiologyCertificate)
from ...utils.custom.admin.actions import export_as_csv_action


class AdmissionInline(admin.TabularInline):
    model = Admission
    extra = 1
    autocomplete_fields = ['destination', 'major']


class EducationInline(GenericTabularInline):
    model = Education
    autocomplete_fields = ('university', 'major')
    extra = 1


class RegularLanguageCertificateInline(GenericTabularInline):
    model = RegularLanguageCertificate
    extra = 1


class GMATCertificateInline(GenericTabularInline):
    model = GMATCertificate
    extra = 1


class GREGeneralCertificateInline(GenericTabularInline):
    model = GREGeneralCertificate
    extra = 1


class GRESubjectCertificateInline(GenericTabularInline):
    model = GRESubjectCertificate
    extra = 1


class GREBiologyCertificateInline(GenericTabularInline):
    model = GREBiologyCertificate
    extra = 1


class GREPhysicsCertificateInline(GenericTabularInline):
    model = GREPhysicsCertificate
    extra = 1


class GREPsychologyCertificateInline(GenericTabularInline):
    model = GREPsychologyCertificate
    extra = 1


class DuolingoCertificateInline(GenericTabularInline):
    model = DuolingoCertificate
    extra = 1


class PublicationInline(GenericTabularInline):
    model = Publication
    extra = 1


@admin.register(ApplyProfile)
class ApplyProfileAdmin(admin.ModelAdmin):
    inlines = [
        AdmissionInline,

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

    # actions = [
    #     export_as_csv_action(
    #         "Similar Profiles CSV Export",
    #         fields=['id', 'name', 'gap', '', 'user__phone_number',
    #                 'last_education__gpa', 'last_education__university__country', 'last_education__university__name',
    #                 get_destination_countries,
    #                 get_destination_universities,
    #                 get_similar_admission,
    #                 ],
    #         file_name='Forms_Similar_Profiles_' + str(datetime.now()),
    #     )
    # ]


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['destination', 'major']
    actions = [
        export_as_csv_action(
            "Similar Profiles CSV Export",
            fields=['id', 'apply_profile_id', 'major', 'grade', 'destination',
                    'accepted', 'scholarship', 'enroll_year',
                    ],
            file_name='Admissions_' + str(datetime.now()),
        )
    ]
