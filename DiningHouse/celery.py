__author__ = '祥祥'

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Executes every Monday noon at 11:27 A.M
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=11, minute=27, day_of_week=[0,1,2,3,4,5,6]),
        'args': (16, 16),
    },
}