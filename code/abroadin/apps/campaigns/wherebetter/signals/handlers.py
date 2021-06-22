from django.db.models import F
from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth import get_user_model

User = get_user_model()

from abroadin.apps.campaigns.wherebetter.models import RedeemCode, AppliedRedeemCode, Participant, InviteInfo


def post_save_applied_redeem_code(sender, instance: AppliedRedeemCode, *args, **kwargs):
    instance.redeem_code.usages += 1
    instance.redeem_code.save()
    instance.participant.available_rounds += 1
    instance.participant.save()


def post_delete_applied_redeem_code(sender, instance, *args, **kwargs):
    instance.redeem_code.usages -= 1
    instance.redeem_code.save()
    instance.participant.available_rounds -= 1
    instance.participant.save()


def pre_save_user(sender, instance, *args, **kwargs):
    def process_user_invite_info():
        # Check if user has successful invites before.
        if InviteInfo.objects.filter(invited_user=instance, approved=True).exists():
            return

        invite_info = InviteInfo.objects.filter(invited_user=instance, approved=False).order_by('invite_date').first()
        if invite_info:
            invite_info.approved = True
            invite_info.save()

    if instance._state.adding is True and instance._state.db:
        if instance.is_email_verified:
            process_user_invite_info()
    else:
        db_instance = User.objects.get(pk=instance.pk)
        if db_instance.is_email_verified != instance.is_email_verified and instance.is_email_verified:
            process_user_invite_info()


def pre_save_participant(sender, instance, *args, **kwargs):
    if instance._state.adding is True and instance._state.db:
        instance.referral_id = Participant.get_random_ref()


def pre_save_invite_info(sender, instance: InviteInfo, *args, **kwargs):
    if instance._state.adding is True and instance._state.db:
        if instance.approved or instance.invited_user.is_email_verified:
            instance.approved = True
            instance.apply_extra_round_to_invitor()
    else:
        db_instance = InviteInfo.objects.get(pk=instance.pk)
        if db_instance.approved != instance.approved and instance.approved:
            instance.apply_extra_round_to_invitor()


pre_save.connect(pre_save_participant, Participant)
pre_save.connect(pre_save_invite_info, InviteInfo)
pre_save.connect(pre_save_user, User)

post_save.connect(post_save_applied_redeem_code, AppliedRedeemCode)
post_delete.connect(post_delete_applied_redeem_code, AppliedRedeemCode)