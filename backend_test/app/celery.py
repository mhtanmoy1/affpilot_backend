from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

schedule, created = IntervalSchedule.objects.get_or_create(
    every=30,
    period=IntervalSchedule.MINUTES,
)

PeriodicTask.objects.create(
    interval=schedule,
    name="Archive old books",
    task="app.tasks.archive_books",
    args=json.dumps([]),
)
