from django.contrib import admin

from . import models


@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__id', 'user__first_name']


@admin.register(models.RedeemCode)
class RedeemCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'active', 'usages')


@admin.register(models.AppliedRedeemCode)
class AppliedRedeemCodeAdmin(admin.ModelAdmin):
    search_fields = ['participant__user__email', 'participant__user__id', 'participant__user__first_name',
                     'redeem_code__code']

    list_display = ('id', 'participant', 'redeem_code')


@admin.register(models.InviteInfo)
class InviteInfoModelAdmin(admin.ModelAdmin):
    list_filter = ['origin']
    list_display = ['id', 'invitor_user', 'invited_user']
    search_fields = ['invitor_user__email', 'invitor_user__first_name',
                     'invited_user__email', 'invited_user__first_name']
