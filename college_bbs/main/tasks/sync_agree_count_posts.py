from college_bbs.celery import bbs_task
from college_bbs.common.redis_conn import CONN
from college_bbs.common.views import get_redis_bitmap_key
from main.models import Post


@bbs_task
def sync_post_agree_count():
    """
    同步文章点赞量
    """
    posts = Post.objects.all()
    objs = []
    for query in posts:
        redis_bit_key = get_redis_bitmap_key(query.id, "post_agree")
        agree_count = CONN.bitcount(redis_bit_key)
        if query.agree_number != agree_count:
            query.agree_number = agree_count
            objs.append(query)
    Post.objects.bulk_update(objs, ["agree_number"])
