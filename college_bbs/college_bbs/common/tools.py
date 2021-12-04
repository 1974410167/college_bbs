from college_bbs.common.redis_conn import CONN
import time


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class HandleViewsCount:

    def __init__(self, instance, request):
        self.instance = instance
        self.request = request

    def run(self):
        return self.handle_views_count()

    def handle_views_count(self):
        """
        把关于用户地址的字符串加入hyperloglog并更新post_views_count对应id的值
        """
        hyper_key, redis_key_string = self.get_key()
        CONN.pfadd(hyper_key, redis_key_string)
        views_count = CONN.pfcount(hyper_key)
        return views_count

    def get_key(self):
        """
        获得hyperloglog的key和向hyperloglog Put的值
        """
        hyper_key = get_hyper_key(self.instance)
        client_id = get_client_ip(self.request)
        current_year = time.localtime().tm_year
        current_mon = time.localtime().tm_mon
        current_day = time.localtime().tm_mday
        current_hour = time.localtime().tm_hour
        current_min = time.localtime().tm_min // 10
        redis_key_string = client_id + "_" + str(current_hour) + "_" + str(current_day) + "_" + str(current_mon) + "_" + str(current_year) + str(current_min)
        return hyper_key, redis_key_string


def get_hyper_key(instance):
    """
    根据id和标题组建key
    """
    id = instance.id
    title = instance.title
    hyper_key = title + "_" + str(id)
    return hyper_key


def sync_pageviews(queryset):

    for query in queryset:
        hyper_key = get_hyper_key(query)
        redis_views_count_pfcount = CONN.pfcount(hyper_key)
        query.views_count = redis_views_count_pfcount
