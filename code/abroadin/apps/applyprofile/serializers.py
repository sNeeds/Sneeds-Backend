from rest_framework import serializers

from .models import ApplyProfile, Admission


class ApplyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplyProfile
        fields = ['id', 'name', 'academic_gap',
                  # 'publications', 'educations',
                  ]


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission
        fields = [
            'id', 'enrolled', 'origin_university', 'destination_university',
            'scholarships', 'scholarships_unit', 'major',
            'accepted', 'description', 'choose_reason',
        ]
