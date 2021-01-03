from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import ApplyProfile, Admission
from abroadin.apps.data.applydata.models import (
    Publication, Education, RegularLanguageCertificate, GMATCertificate, DuolingoCertificate,
    GRESubjectCertificate, GREGeneralCertificate, GREPsychologyCertificate, GREPhysicsCertificate,
    GREBiologyCertificate)


class AdmissionInline(admin.TabularInline):
    model = Admission
    extra = 1
    autocomplete_fields = ['origin_university', 'destination_university', 'major']


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
