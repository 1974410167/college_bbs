from django.core.management.base import BaseCommand
from django.db import transaction
from main.models import Topic, Post, ParentComment, ChildComment

from faker import Faker
import random

from user.models import UserProfile

fake = Faker(locale='zh_CN')


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        python manage.py generate_data
        """
        with transaction.atomic():
            user_ids = UserProfile.objects.values_list("id", flat=True)
            topics = ["考研", "交友", "寻物启事", "健身", "篮球", "足球", "英雄联盟", "csgo", "绝地求生", "王者荣耀"]
            topic_objs = []
            for topic in topics:
                t = Topic(name=topic)
                t.save()
                topic_objs.append(t)
            print(f"生成{len(topic_objs)}条话题")

            post_objs = []
            for _ in range(1000):
                p = Post()
                topic_obj = random.choice(topic_objs)
                p.topic_id = topic_obj.id
                p.title = topic_obj.name + "title" + str(_)
                p.content = topic_obj.name + "content" + str(_)
                p.create_user_id = random.choice(user_ids)
                p.save()
                post_objs.append(p)
            print(f"生成{len(post_objs)}条帖子")

            parent_comment = []
            for _ in range(5000):
                c = ParentComment()
                post_obj = random.choice(post_objs)
                c.content = post_obj.content + "_comment" + str(_)
                c.post_id = post_obj.id
                c.create_user_id = random.choice(user_ids)
                c.save()
                post_obj.answer_count += 1
                post_obj.save()
                parent_comment.append(c)
            print(f"生成{len(parent_comment)}条帖子的评论")

            child_comments = []
            for _ in range(8000):
                child = ChildComment()
                parent_obj = random.choice(parent_comment)
                child.content = parent_obj.content + "child" + str(_)
                child.parent_comment_id = parent_obj.id
                child.create_user_id = random.choice(user_ids)
                child.save()
                parent_obj.comment_number += 1
                parent_obj.save()
                child_comments.append(child)
            print(f"生成{len(child_comments)}条帖子的评论的回复")

            for _ in range(10000):
                child_comment = ChildComment()
                child_1 = random.choice(child_comments)
                child_comment.content = child_1.content + "child" + str(_)
                child_comment.comment_id = child_1.id
                child_comment.parent_comment_id = child_1.parent_comment_id
                child_comment.create_user_id = random.choice(user_ids)
                child_comment.save()
            print(f"生成10000条帖子的评论的回复的回复")

