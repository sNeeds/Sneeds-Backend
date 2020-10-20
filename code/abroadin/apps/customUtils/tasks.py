from celery import shared_task

from django.core.management import call_command


@shared_task
def backup_database():
    from abroadin.settings.config.variables import SERVER_NAME
    server_name_args = "-s=" + SERVER_NAME
    call_command('dbbackup', server_name_args)


@shared_task
def media_backup():
    from abroadin.settings.config.variables import SERVER_NAME
    server_name_args = "-s=" + SERVER_NAME
    call_command('mediabackup', server_name_args)
