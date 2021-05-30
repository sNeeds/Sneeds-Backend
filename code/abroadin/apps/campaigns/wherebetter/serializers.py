from rest_framework import serializers

from .models import Participant, AppliedRedeemCodes
from abroadin.apps.users.customAuth.serializers import SafeUserDataSerializer


class ParticipantRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Participant
        fields = ['id', 'user']


class SafeParticipantSerializer(serializers.ModelSerializer):
    user = SafeUserDataSerializer()

    class Meta:
        model = Participant
        fields = ['id', 'user', 'score']


class ParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Participant
        fields = ['id', 'user', 'score', '']