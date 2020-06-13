from django.urls import path
from .views import *

urlpatterns = [
    path('', PixelView.as_view()),
    path('rects/', RectangleView.as_view()),
    path('rects/<int:rect_id>', RectangleView.as_view()),
]
