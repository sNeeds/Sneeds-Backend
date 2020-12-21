from datetime import timedelta
from verification.base import CELERY_BEAT_SCHEDULE as VERIFICATION_CELERY_BEAT_SCHEDULE

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_TIMEZONE = 'UTC'

# Other Celery settings
CELERY_BEAT_SCHEDULE = {
    'database-regular-backup': {
        'task': 'abroadin.apps.customUtils.tasks.backup_database',
        'schedule': timedelta(days=1),
    },
    'media-regular-backup': {
        'task': 'abroadin.apps.customUtils.tasks.media_backup',
        'schedule': timedelta(days=1),
    },
    'send-email-notifications': {
        'task': 'abroadin.apps.notifications.tasks.send_email_notifications',
        'schedule': timedelta(seconds=5),
    },
    'update-student-detailed-info-ranks': {
        'task': 'abroadin.apps.estimation.form.tasks.update_student_detailed_info_ranks',
        'schedule': timedelta(hours=24),
    }
}

CELERY_BEAT_SCHEDULE.update(VERIFICATION_CELERY_BEAT_SCHEDULE)
