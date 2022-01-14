from college_bbs.celery import bbs_task
from college_bbs.common.redis_conn import CONN
from main.models import ParentComment


@bbs_task
def sync_comment_agree_count():
    """
    同步评论点赞量
    """
    comments = ParentComment.objects.all()
    objs = []
    for query in comments:
        redis_bit_key = query.id
        agree_count = CONN.bitcount(redis_bit_key)
        if query.like_count != agree_count:
            query.like_count = agree_count
            objs.append(query)
    ParentComment.objects.bulk_update(objs, ["like_count"])
