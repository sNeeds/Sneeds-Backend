from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model

User = get_user_model()

from abroadin.apps.campaigns.wherebetter.models import RedeemCode, AppliedRedeemCodes, Participant, InviteInfo


def post_save_applied_redeem_code(sender, instance, *args, **kwargs):
    RedeemCode.objects.filter(id=instance.redeem_code.id).update(usages=F('usages') + 1)


def post_delete_applied_redeem_code(sender, instance, *args, **kwargs):
    RedeemCode.objects.filter(id=instance.redeem_code.id).update(usages=F('usages') - 1)


# def post_save_user(sender, instance, *args, **kwargs):
    # if instance._state.adding is True and instance._state.db:
    #     if instance.is_email_verified:
    # if instance.is_email_verified:
    #     try:
    #         participant = Participant.objects.get(user=instance)
    #         invite_infos = list(InviteInfo.objects.filter(invited=participant, approved=True).
    #                             values_list('id', 'invitor', 'invite_date'))
    #         invite_infos.sort(key=lambda x: x[2])




post_save.connect(post_save_applied_redeem_code, AppliedRedeemCodes)
post_delete.connect(post_delete_applied_redeem_code, AppliedRedeemCodes)