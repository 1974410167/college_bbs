from django.contrib import admin

from user.models import UserProfile
from .models import Topic, Post, ChildComment, ParentComment
from django import forms


admin.site.site_header = '西亚斯校园论坛'
admin.site.site_title = "主要内容"
admin.site.index_title = "论坛管理目录"


class PostForm(forms.ModelForm):
    topic_name = forms.CharField(required=True, max_length=125, help_text="topic_name")

    class Meta:
        model = Post
        # fields = ('content', 'views_count', 'agree_number', "topic_id", "topic")
        exclude = ("create_time", )


class PostAdmin(admin.ModelAdmin):
    list_display = ("content", "views_count", "agree_number", "topic", "create_user", )
    ordering = ('-agree_number',)
    list_filter = ('content',)
    fields = ('content', 'views_count', 'agree_number', "topic_id",)
    search_fields = ('content',)
    readonly_fields = ["topic", "create_user"]

    @admin.display(description="话题")
    def topic(self, obj):
        topic_id = obj.topic_id
        q = Topic.objects.filter(id=topic_id).first()
        if q:
            return q.name
        else:
            return "-"

    @admin.display(description="创建人")
    def create_user(self, obj):
        user_id = obj.create_user_id
        q = UserProfile.objects.filter(id=user_id).first()
        if q:
            return q.name
        else:
            return "-"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fields = ('content', 'views_count', 'agree_number', "topic_id", "topic", "create_user")
        self.readonly_fields = ["topic", "create_user"]
        return super(PostAdmin, self).change_view(request, object_id, form_url='', extra_context=None)


class ParentCommentAdmin(admin.ModelAdmin):
    list_display = ("content", "create_user",)
    list_filter = ('content', )
    fields = ('content', "create_user")
    readonly_fields = ["create_user"]
    search_fields = ["content"]

    @admin.display(description="创建人")
    def create_user(self, obj):
        user_id = obj.create_user_id
        q = UserProfile.objects.filter(id=user_id).first()
        if q:
            return q.name
        else:
            return "-"


class ChildCommentAdmin(ParentCommentAdmin):
    pass


class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "host_number", "create_user")
    ordering = ('-host_number',)
    list_filter = ('name',)
    fields = ["name", "description"]
    search_fields = ('name',)

    @admin.display(description="创建人")
    def create_user(self, obj):
        user_id = obj.create_user_id
        q = UserProfile.objects.filter(id=user_id).first()
        if q:
            return q.name
        else:
            return "-"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fields = ('name', 'description', 'host_number', "create_user")
        self.readonly_fields = ["create_user"]
        return super(TopicAdmin, self).change_view(request, object_id, form_url='', extra_context=None)


admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ChildComment, ChildCommentAdmin)
admin.site.register(ParentComment, ParentCommentAdmin)
