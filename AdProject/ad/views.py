from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView,View
from django.http import HttpResponse
# Create your views here.

class AdDetail(DetailView):
    model = Ad
    template_name = 'Ad.html'
    context_object_name = 'ad'

class AdList(ListView):
    model = Ad
    ordering = '-date'
    context_object_name = 'ad'
    paginate_by = 10
    template_name = 'all_ads.html'

class CreateAnswer(View):

    def get(self, request, *args, **kwargs):
        # получаю ид объявления на которое отвечают
        id = 0
        for pk, number in kwargs.items():
            id = int(number)
        to_html = {'text': f'Вы отвечаете на объявление: {Ad.objects.get(id = id).header}'}
        return render(request, 'create_answer.html', context=to_html)

    def post(self,request, *args, **kwargs):
        id_ad = 0
        for pk, number in kwargs.items():
            id_ad = int(number)
        ad_instance = Ad.objects.get(id = id_ad)
        user_from = request.POST['user']
        user_from = User.objects.get(username=f'{user_from}')
        text_from = request.POST['text']
        new_answer = Answer(
            user= user_from,
            ad = ad_instance,
            text = text_from,
        )
        try:
            new_answer.save()
        except:
            return HttpResponse('что то пошло не так')


        return HttpResponse('vse chiki piki')







