from django.urls import path

from parse.views import ozon_parse

urlpatterns = [
    path('parse', ozon_parse, name='parse')
]
