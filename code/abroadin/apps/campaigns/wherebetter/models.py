from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class RedeemCode(models.Model):
    active = models.BooleanField(default=True)
    code = models.CharField(max_length=32)
    usage_limit = models.IntegerField(default=2000)
    usages = models.IntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    score = models.IntegerField(default=0)
    available_rounds = models.IntegerField(default=1)
    redeem_codes = models.ManyToManyField(RedeemCode, through='AppliedRedeemCodes')
    invited_participants = models.ManyToManyField(User, through='InviteInfo')


class AppliedRedeemCodes(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    redeem_code = models.ForeignKey(RedeemCode, on_delete=models.CASCADE)
    apply_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('participant', 'redeem_code')


class InviteInfo(models.Model):
    class Origin(models.TextChoices):
        TELEGRAM = 'Telegram', 'Telegram'
        FACEBOOK = 'Facebook', 'Facebook'
        LINKEDIN = 'Linkedin', 'Linkedin'
        TWITTER = 'Twitter', 'Twitter'
        INSTAGRAM = 'Instagram', 'Instagram'

    invitor = models.ForeignKey(Participant, on_delete=models.CASCADE)
    invited = models.ForeignKey(Participant, on_delete=models.CASCADE)
    origin = models.CharField(choices=Origin.choices, null=True, blank=True)

    class Meta:
        unique_together = ('invitor', 'invited')


class UsedFeatures(models.Model):
    class Feature(models.TextChoices):
        ANALYZE = 'Analyze'

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    feature = models.CharField(Feature.choices)
    date = models.DateTimeField(auto_now=True, auto_created=True)


class Play(models.Model):
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True, auto_created=True)
    duration = models.SmallIntegerField(default=0, help_text='In seconds')
    answered_questions = ArrayField(models.PositiveSmallIntegerField(), null=True, blank=True)




