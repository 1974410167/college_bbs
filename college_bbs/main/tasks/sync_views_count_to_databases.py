from college_bbs.celery import bbs_task
from college_bbs.common.redis_conn import CONN
from college_bbs.common.tools import get_hyper_key
from main.models import Post


@bbs_task
def sync_posts_views_count():
    """
    同步帖子浏览量
    """
    posts = Post.objects.all()
    objs = []
    for query in posts:
        if query.views_count != 0:
            hyper_key = get_hyper_key(query)
            redis_views_count_pfcount = CONN.pfcount(hyper_key)
            if query.views_count != redis_views_count_pfcount:
                query.views_count = redis_views_count_pfcount
                objs.append(query)
    Post.objects.bulk_update(objs, ["views_count"])
