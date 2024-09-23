from rest_framework.pagination import PageNumberPagination


class ReviewPagination(PageNumberPagination):
    """
    Custom pagination class for reviews, setting a default page size and allowing clients to specify page size via query parameters.
    """

    page_size = 20
    page_size_query_param = "size"
    max_page_size = 20