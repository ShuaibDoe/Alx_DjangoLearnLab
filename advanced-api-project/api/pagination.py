from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # default items per page
    page_size_query_param = 'page_size'  # client can override like ?page_size=20
    max_page_size = 100  # prevent abuse
    page_query_param = 'p'  # instead of ?page=2 you can use ?p=2
