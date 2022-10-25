from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class LimitPagePagination(PageNumberPagination):
    '''Paginator.'''
    page_size = settings.RECORDS_ON_PAGE
    page_size_query_param = 'limit'