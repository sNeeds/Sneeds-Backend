import uuid

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils.crypto import get_random_string

from abroadin.apps.campaigns.wherebetter.constants import PARTICIPANT_REFERRAL_CHARS

User = get_user_model()


class RedeemCode(models.Model):
    active = models.BooleanField(default=True)
    code = models.CharField(unique=True, max_length=32)
    usage_limit = models.IntegerField(default=2000)
    usages = models.IntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True)
    available_rounds = models.IntegerField(default=1)
    redeem_codes = models.ManyToManyField(RedeemCode, through='AppliedRedeemCode')
    referral_id = models.CharField(max_length=8)

    @classmethod
    def get_random_ref(cls):
        s = get_random_string(length=8, allowed_chars=PARTICIPANT_REFERRAL_CHARS)
        if cls.objects.filter(referral_id=s).exists():
            return cls.get_random_ref()
        return s


class AppliedRedeemCode(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    redeem_code = models.ForeignKey(RedeemCode, on_delete=models.CASCADE)
    apply_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participant', 'redeem_code')


class InviteOrigin(models.TextChoices):
    TELEGRAM = 'Telegram', 'Telegram'
    FACEBOOK = 'Facebook', 'Facebook'
    LINKEDIN = 'Linkedin', 'Linkedin'
    TWITTER = 'Twitter', 'Twitter'
    INSTAGRAM = 'Instagram', 'Instagram'


class InviteInfo(models.Model):
    invitor_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_as_invitor")
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_as_invited")
    origin = models.CharField(max_length=16, choices=InviteOrigin.choices, null=True, blank=True)
    invite_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('invitor_user', 'invited_user')

    def apply_extra_round_to_invitor(self):
        Participant.objects.filter(user=self.invitor_user).update(available_rounds=F('available_rounds') + 1)


class UsedFeatures(models.Model):
    class Feature(models.TextChoices):
        ANALYZE = 'Analyze'

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    feature = models.CharField(max_length=32, choices=Feature.choices)
    date = models.DateTimeField(auto_now=True, auto_created=True)


class Play(models.Model):
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True, auto_created=True)
    duration = models.SmallIntegerField(default=0, help_text='In seconds')
    answered_questions = ArrayField(models.PositiveSmallIntegerField(), null=True, blank=True)
