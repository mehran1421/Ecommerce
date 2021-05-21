from rest_framework.pagination import LimitOffsetPagination


class PaginationTools(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
    limit_query_param = "limit"
    offset_query_param = "offset"
