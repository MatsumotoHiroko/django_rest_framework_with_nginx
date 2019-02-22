# coding: utf-8

from rest_framework_nested import routers
from .views import BookViewSet, RateViewSet, login
from django.conf.urls import url, include
from django.urls import path

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)

books_router = routers.NestedSimpleRouter(router, r'books', lookup='book')
books_router.register(r'rating', RateViewSet, base_name='books-rates')

urlpatterns = [
    path('login', login),
    url(r'^', include(router.urls)),
    url(r'^', include(books_router.urls)),
]