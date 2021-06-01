from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Participant, AppliedRedeemCodes, RedeemCode
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
    applied_redeem_codes = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = ['id', 'user', 'score', 'applied_redeem_codes']

    def get_applied_redeem_codes(self, obj):
        return


class AppliedRedeemCodesRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedRedeemCodes
        fields = ['id', 'participant', 'redeem_code', 'apply_date']

    def validate_redeem_code(self, value):
        try:
            redeem_code = RedeemCode.objects.get(code=value)
        except RedeemCode.DoesNotExist():
            raise ValidationError("Redeem code doesn't exist.")

        if not redeem_code.active:
            raise ValidationError("Redeem code is not active.")

        if redeem_code.usage_limit - redeem_code.usages < 1:
            raise ValidationError("Redeem code usage limit has reached to zero. :(")

        now = datetime.now()

        if now < redeem_code.start_date:
            raise ValidationError("Redeem code is not usable yet.")

        if now > redeem_code.expiration_date:
            raise ValidationError("Redeem code is expired.")

        return value

    def validate_participant(self, value: Participant):
        assert self.context is not None, "context is None"
        assert self.context.get('request') is not None, "context['request'] is None"
        if self.context['request'].user != value.user:
            raise ValidationError("Only the participant himself can apply redeem code.")
        return Participant

    def validate(self, attrs):
        qs = AppliedRedeemCodes.objects.filter(participant=attrs['participant'],
                                               redeem_code__code=attrs['redeem_code'])
        if qs.exists():
            raise ValidationError("You used this code before.")

        return attrs
