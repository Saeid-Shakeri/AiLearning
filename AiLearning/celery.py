from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# تنظیمات پیش‌فرض جنگو برای Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AiLearning.settings')

app = Celery('AiLearning')

# app.conf.beat_schedule = {
#     'send-monthly-report': { # enable email configuration
#         'task': 'course.tasks.send_monthly_report',
#         'schedule': crontab(day_of_month=1),  # روز اول هر ماه
#         'args': (['admin1@example.com', 'admin2@example.com'],),
    
#     },
# }

# استفاده از تنظیمات جنگو برای تنظیم Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# بارگذاری خودکار تماری از تمام اپ‌ها
app.autodiscover_tasks()

