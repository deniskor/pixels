from django.urls import path
from .views import *

urlpatterns = [
    path('', PixelView.as_view()),
]
