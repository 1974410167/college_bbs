from django.core.management import BaseCommand
from django.db import transaction
from main.models import Topic, Post, ParentComment, ChildComment


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        python manage.py delete_database_main_data
        """
        with transaction.atomic():
            ChildComment.objects.all().delete()
            print("表ChildComment数据被清空")
            ParentComment.objects.all().delete()
            print("表ParentComment数据被清空")
            Post.objects.all().delete()
            print("表Post数据被清空")
            Topic.objects.all().delete()
            print("表Topic数据被清空")
