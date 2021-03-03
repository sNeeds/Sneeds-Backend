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


def apply_profile_publications(apply_profile):
    return list(apply_profile.publications.all().only('id'))


def apply_profile_publications_count(apply_profile):
    return apply_profile.publications.all().count()


def apply_profile_language(apply_profile):
    return list(apply_profile.language_certificates.all().values_list('certificate_type'))


def apply_profile_admissions(apply_profile):
    return list(apply_profile.admissions.all().values_list('id', flat=True))


def apply_profile_educations_ordered(apply_profile):
    return list(apply_profile.educations.all().order_by_grade().values_list('id', flat=True))


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

    actions = [
        export_as_csv_action(
            "CSV Export",
            fields=['id', 'name', 'gap',
                    'last_education__id', 'main_admission__id',
                    'bachelor_education__id', 'master_education__id', 'phd_education__id', 'post_doc_education__id',
                    apply_profile_admissions,
                    apply_profile_publications_count,
                    apply_profile_publications,
                    apply_profile_language,
                    ],
            file_name='Apply_Profiles_' + str(datetime.now()),
        )
    ]


def get_admission_major(admission):
    return admission.major.name.strip()


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['destination', 'major']
    actions = [
        export_as_csv_action(
            "CSV Export",
            fields=['id', 'apply_profile_id', get_admission_major, 'grade', 'destination',
                    'accepted', 'scholarship', 'enroll_year',
                    ],
            file_name='Admissions_' + str(datetime.now()),
        )
    ]
