from rest_framework import serializers

from abroadin.apps.data.applydata.models import Publication

from .models import ApplyProfile, Admission


class ApplyProfileSerializer(serializers.ModelSerializer):
    admissions = serializers.SerializerMethodField(
        method_name='get_admissions',
    )

    publications = serializers.SerializerMethodField(
        method_name='get_publications',
    )

    class Meta:
        model = ApplyProfile
        fields = ['id', 'name', 'academic_gap',
                  'admissions',
                  'publications',
                  # 'educations',
                  ]

    def get_admissions(self, obj: ApplyProfile):
        print(obj.publications.all)
        return AdmissionSerializer(obj.admission_set.all(), context=self.context, many=True).data


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission
        fields = [
            'id', 'apply_profile', 'enroll_year', 'origin_university', 'destination_university',
            'scholarships', 'scholarships_unit', 'major',
            'accepted', 'description',
        ]
