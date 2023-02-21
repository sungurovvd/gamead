from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('ad/<int:pk>', AdDetail.as_view(), name = 'ad_detail'),
    path('ad/<int:pk>/update', UpdateAd.as_view(), name = 'update_ad'),
    path('ad/create', CreateAd.as_view(), name = 'create_ad'),
    path('', AdList.as_view(), name = 'ad_list'),
    path('ad/<int:pk>/create_answer', CreateAnswer.as_view(), name = 'create_answer'),
    path('answer/tomyad', AnswersToMyAd.as_view(), name = 'answer_to_my_ad'),
    path('answer/my', MyAnswers.as_view(), name = 'my_answer'),
    path('answer/<int:pk>', AnswerDetail.as_view(), name = 'answer_detail'),
    path('answer/<int:pk>/confirm_answer', ConfirmAnswer.as_view(), name = 'confirm_answer'),
    path('answer/<int:pk>/delete_answer', DeleteAnswer.as_view(), name = 'delete_answer'),
]