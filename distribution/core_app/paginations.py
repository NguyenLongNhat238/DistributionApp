from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class BasePagination(pagination.PageNumberPagination):
    """
    reference link: https://www.sankalpjonna.com/learn-django/pagination-made-easy-with-django-rest-framework
    && also link: https://stackoverflow.com/questions/46916128/how-do-you-paginate-a-viewset-using-a-paginator-class
    """

    page_size = 16
    page_query_param = "page"

    # ordering = ''

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
