from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('ad/<int:pk>', AdDetail.as_view(), name = 'ad_detail'),
    path('ad', AdList.as_view(), name = 'ad_list'),
    path('ad/<int:pk>/create_answer', CreateAnswer.as_view(), name = 'create_answer'),
]