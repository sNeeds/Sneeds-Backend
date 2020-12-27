from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import ApplyProfile
from ...data.applyData.models import (
    Publication, Education, RegularLanguageCertificate, GMATCertificate, DuolingoCertificate,
    GRESubjectCertificate, GREGeneralCertificate, GREPsychologyCertificate, GREPhysicsCertificate,
    GREBiologyCertificate, Admission)


class AdmissionInline(GenericTabularInline):
    model = Admission
    extra = 1
    autocomplete_fields = ['origin_university', 'goal_university', 'major']


class EducationInline(GenericTabularInline):
    model = Education
    autocomplete_fields = ('university', 'major')
    extra = 1


class RegularLanguageCertificateTypeInline(GenericTabularInline):
    model = RegularLanguageCertificate
    extra = 1


class GMATCertificateTypeInline(GenericTabularInline):
    model = GMATCertificate
    extra = 1


class GREGeneralCertificateTypeInline(GenericTabularInline):
    model = GREGeneralCertificate
    extra = 1


class GRESubjectCertificateTypeInline(GenericTabularInline):
    model = GRESubjectCertificate
    extra = 1


class GREBiologyCertificateTypeInline(GenericTabularInline):
    model = GREBiologyCertificate
    extra = 1


class GREPhysicsCertificateTypeInline(GenericTabularInline):
    model = GREPhysicsCertificate
    extra = 1


class GREPsychologyCertificateTypeInline(GenericTabularInline):
    model = GREPsychologyCertificate
    extra = 1


class DuolingoCertificateTypeInline(GenericTabularInline):
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

        RegularLanguageCertificateTypeInline,
        GMATCertificateTypeInline,
        GREGeneralCertificateTypeInline,
        GRESubjectCertificateTypeInline,
        GREBiologyCertificateTypeInline,
        GREPhysicsCertificateTypeInline,
        GREPsychologyCertificateTypeInline,
        DuolingoCertificateTypeInline,
    ]
