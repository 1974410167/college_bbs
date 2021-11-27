from rest_framework.response import Response
from college_bbs.common.data_fetch import DataFetch


class DataFetchListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            DataFetch(data, self.model, self.configs).main_loop()
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        DataFetch(data, self.model, self.configs).main_loop()
        return Response(data)


class DataFetchRetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        DataFetch(data, self.model, self.configs).main_loop()
        return Response(data)
