
from django.urls import path

from sharemypic.web.views import index

urlpatterns = [
    path('', index, name='index')
]
