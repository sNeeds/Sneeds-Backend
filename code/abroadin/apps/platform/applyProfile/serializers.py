from rest_framework import serializers

from .models import ApplyProfile


class ApplyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplyProfile
        fields = ['id', 'show_name', 'latest_degree',
                  # 'publications', 'educations',
                  ]
