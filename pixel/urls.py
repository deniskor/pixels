from django.urls import path
from .views import *

urlpatterns = [
    path('set', set_color),
    path('get', get_color),
    path('put', change_color),
    path('del', delete_color),
]
