from django.contrib import admin

from django.contrib import admin

from .models import EmailNotification


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ['email', 'sent', 'send_date']
    readonly_fields = ['created', 'updated', 'sent', 'data_json', 'get_data_dict']
