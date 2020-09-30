from datetime import timedelta

from celery.schedules import crontab

# https://stackoverflow.com/questions/21631878/celery-is-there-a-way-to-write-custom-json-encoder-decoder
# Register your new serializer methods into kombu
from kombu.serialization import register
from sNeeds.settings.celery.serializers import c_dumps, c_loads

# register('cjson', c_dumps, c_loads,
#          content_type='application/x-cjson',
#          content_encoding='utf-8')

# Tell celery to use your new serializer:
# CELERY_ACCEPT_CONTENT = ['cjson']
# CELERY_TASK_SERIALIZER = 'cjson'
# CELERY_RESULT_SERIALIZER = 'cjson'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_TIMEZONE = 'UTC'

# Other Celery settings
CELERY_BEAT_SCHEDULE = {
    'create-room': {
        'task': 'sNeeds.apps.videochats.tasks.create_rooms_from_sold_time_slots',
        'schedule': timedelta(minutes=1),
    },
    'delete-room': {
        'task': 'sNeeds.apps.videochats.tasks.delete_used_rooms',
        'schedule': timedelta(minutes=1),
    },
    'delete-time-slots': {
        'task': 'sNeeds.apps.store.tasks.delete_time_slots',
        'schedule': timedelta(minutes=1),
    },
    'database-regular-backup': {
        'task': 'sNeeds.apps.customUtils.tasks.backup_database',
        'schedule': timedelta(days=1),
    },
    'media-regular-backup': {
        'task': 'sNeeds.apps.customUtils.tasks.media_backup',
        'schedule': timedelta(days=1),
    },
    'send-email-notifications': {
        'task': 'sNeeds.apps.notifications.tasks.send_email_notifications',
        'schedule': timedelta(seconds=5),
    },
}
