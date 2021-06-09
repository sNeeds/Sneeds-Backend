from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django.db.utils import OperationalError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from abroadin.apps.users.customAuth.serializers import SafeUserDataSerializer, UserSerializer

from .models import Participant, AppliedRedeemCode, RedeemCode, InviteInfo


class ParticipantRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Participant
        fields = ['id', 'user']


class SafeParticipantSerializer(serializers.ModelSerializer):
    user = SafeUserDataSerializer()

    class Meta:
        model = Participant
        fields = ['id', 'user', 'score', 'rank']


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    applied_redeem_codes = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = ['id', 'user', 'score', 'applied_redeem_codes']

    def get_applied_redeem_codes(self, obj: Participant):
        obj.user.all().values_list('redeem_code__code')


class AppliedRedeemCodesRequestSerializer(serializers.ModelSerializer):
    redeem_code_text = serializers.CharField(max_length=32)

    class Meta:
        model = AppliedRedeemCode
        fields = ['id', 'participant', 'redeem_code_text', 'apply_date']

    def validate_redeem_code_text(self, value):
        try:
            redeem_code = RedeemCode.objects.get(code=value)
        except RedeemCode.DoesNotExist():
            raise ValidationError(_("Redeem code doesn't exist."))

        if not redeem_code.active:
            raise ValidationError(_("Redeem code is not active."))

        if redeem_code.usage_limit - redeem_code.usages < 1:
            raise ValidationError(_("Redeem code usage limit has reached to zero. :("))

        now = datetime.now()

        if now < redeem_code.start_date:
            raise ValidationError(_("Redeem code is not usable yet."))

        if now > redeem_code.expiration_date:
            raise ValidationError(_("Redeem code is expired."))

        return value

    def validate_participant(self, value: Participant):
        assert self.context is not None, "context is None"
        assert self.context.get('request') is not None, "context['request'] is None"
        if self.context['request'].user != value.user:
            raise ValidationError(_("Only the participant himself can apply redeem code."))
        return value

    def validate(self, attrs):
        qs = AppliedRedeemCode.objects.filter(participant=attrs['participant'],
                                              redeem_code__code=attrs['redeem_code_text'])
        if qs.exists():
            raise ValidationError(_("You used this code before."))

        return attrs

    def create(self, validated_data):
        validated_data['redeem_code'] = RedeemCode.objects.get(code=validated_data.pop('redeem_code_text'))
        return AppliedRedeemCode.objects.create(**validated_data)


class AppliedRedeemCodesSerializer(serializers.ModelSerializer):
    redeem_code_text = serializers.SerializerMethodField()

    class Meta:
        model = AppliedRedeemCode
        fields = ['id', 'participant', 'redeem_code_text', 'apply_date']
        extra_kwargs = {
            'id': {'read_only': True, },
            'participant': {'read_only': True, },
            'apply_date': {'read_only': True, },
        }

    def get_redeem_code_text(self, obj):
        return obj.redeem_code.code


class InviteInfoRequestSerializer(serializers.ModelSerializer):
    referral_id = serializers.CharField(write_only=True, max_length=8)

    class Meta:
        model = InviteInfo
        fields = ['id', 'referral_id', 'invited_user', 'origin']

    # def validate_referral_id(self, value):
    #     qs = Participant.objects.filter(referral_id=value)
    #     if not qs.exists():
    #         raise ValidationError(_("There is no user with this referral id."))
    #     return value

    def validate_invited_user(self, value):
        assert self.context is not None, "context is None"
        assert self.context.get('request') is not None, "context['request'] is None"
        if self.context['request'].user != value:
            raise ValidationError(_("Request user should be the invited user himself."))
        return value

    def create(self, validated_data):
        try:
            validated_data['invitor_user'] = Participant.objects.select_related('user'). \
                get(referral_id=validated_data.pop('referral_id')).user
        except Participant.DoesNotExist:
            raise ValidationError(_("There is no user with this referral id."))

        if InviteInfo.objects.filter(invited_user=validated_data['invited_user'],
                                     invitor_user=validated_data['invitor_user']
                                     ).exists():
            raise ValidationError(_("The invited user is invited by this invitor before."))

        if InviteInfo.objects.filter(invited_user=validated_data['invited_user'], approved=True).exists():
            raise ValidationError(_("The invited user has been invited completely before."))

        return InviteInfo.objects.create(**validated_data)


class InviteInfoSerializer(serializers.ModelSerializer):
    referral_id = serializers.CharField(write_only=True, max_length=8)

    class Meta:
        model = InviteInfo
        fields = ['id', 'invitor_user', 'invited_user', 'origin']
