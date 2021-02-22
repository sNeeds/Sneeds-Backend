from django.contrib import admin

from . import models

admin.site.register(models.TextMessage)
admin.site.register(models.FileMessage)
admin.site.register(models.VoiceMessage)
admin.site.register(models.ImageMessage)


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "consultant"]
