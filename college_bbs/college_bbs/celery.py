import os
from celery import Celery
from celery.schedules import crontab


def bbs_task(func):
    return app.task(name="bbs." + func.__name__)(func)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_bbs.settings")


app = Celery("bbs")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(
    [
        "user",
        "main"
    ]
)

app.conf.beat_schedule = {
    # 每分钟同步文章浏览量一次
    "sync_posts_views_count": {
        "task": "bbs.sync_posts_views_count",
        "schedule": crontab(minute="*/1"),
    },
    # 每分钟同步评论赞同数一次
    "sync_comment_agree_count": {
        "task": "bbs.sync_comment_agree_count",
        "schedule": crontab(minute="*/1"),
    },
    # 每分钟同步文章赞同数一次
    "sync_post_agree_count": {
        "task": "bbs.sync_post_agree_count",
        "schedule": crontab(minute="*/1"),
    },
    "sync_topic_number": {
        "task": "bbs.sync_topic_number",
        "schedule": crontab(minute="*/1"),
    },
}
