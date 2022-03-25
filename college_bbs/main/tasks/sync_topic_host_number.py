from college_bbs.celery import bbs_task

from main.models import Post, Topic, ParentComment, ChildComment


@bbs_task
def sync_topic_number():
    """
    sync topic host number
    """
    topics = Topic.objects.all()
    objs = []
    if topics:
        for query in topics:
            topic_id = query.id
            values = Post.objects.filter(topic_id=topic_id).values("id", "views_count", "agree_number")
            agree_numbers = [item["agree_number"] for item in values]
            post_ids = [item["id"] for item in values]
            views_counts = [item["views_count"] for item in values]
            parent_comment_ids = ParentComment.objects.filter(post_id__in=post_ids).values_list("id", flat=True)
            child_counts = ChildComment.objects.filter(parent_comment_id__in=parent_comment_ids).count()

            cur_host_numbers = child_counts*3 + sum(views_counts) + len(parent_comment_ids) * 5 + sum(agree_numbers) * 2
            query.host_number = cur_host_numbers
            objs.append(query)

    Topic.objects.bulk_update(objs, ["host_number"])
