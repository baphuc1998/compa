from rest_framework.pagination import PageNumberPagination

class Patigation_1000_item(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class Patigation_100_item(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class Patigation_50_item(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50

class Patigation_10_item(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

class Patigation_5_item(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5