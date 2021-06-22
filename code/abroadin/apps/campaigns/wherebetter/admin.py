from django.contrib import admin

from . import models


admin.site.register(models.Participant)
admin.site.register(models.RedeemCode)
admin.site.register(models.AppliedRedeemCode)
admin.site.register(models.InviteInfo)
