from main.models import Post, ParentComment, ChildComment
from user.authentication import _auth_ctx
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import UserProfile


class UserCenterViewSets(APIView):

    def get(self, request):

        user_id = _auth_ctx.user.userprofile.id
        posts = Post.objects.filter(create_user_id=user_id)
        parent_comments = ParentComment.objects.filter(create_user_id=user_id)
        child_comments = ChildComment.objects.filter(create_user_id=user_id)
        agree_number = sum(posts.values_list("agree_number", flat=True))
        parent_agree_number = sum(parent_comments.values_list("like_count", flat=True))
        child_agree_number = sum(child_comments.values_list("like_count", flat=True))
        made_agree = agree_number + parent_agree_number + child_agree_number
        user_profile = UserProfile.objects.filter(id=user_id).first()
        name = "访客"
        url = "https://v3.cn.vuejs.org/logo.png"

        if user_profile:
            name = user_profile.name if user_profile.name else name
            url = user_profile.circle_url if user_profile.circle_url else url
        return Response({"post_count": posts.count(),
                         "comment_count": parent_comments.count() + child_comments.count(),
                         "made_agree": made_agree,
                         "name": name,
                         "url": url
                         })
