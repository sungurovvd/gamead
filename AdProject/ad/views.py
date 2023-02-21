from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView,View, UpdateView
from PIL import Image
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
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


class CreateAnswer(LoginRequiredMixin, View):
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
        new_answer.save()
        return redirect('ad_list')


class AnswersToMyAd(LoginRequiredMixin, ListView):
    model = Answer
    ordering = '-date'
    context_object_name = 'answers'
    paginate_by = 10
    template_name = 'AnswersToMyAd.html'


class MyAnswers(LoginRequiredMixin, ListView):
    model = Answer
    ordering = '-date'
    context_object_name = 'answers'
    paginate_by = 10
    template_name = 'myanswers.html'


class AnswerDetail(LoginRequiredMixin, DetailView):
    model = Answer
    template_name = 'answer.html'
    context_object_name = 'answer'


class ConfirmAnswer(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # получаю ид объявления на которое отвечают
        id = 0
        for pk, number in kwargs.items():
            id = int(number)
        to_html = {'text': f'Вы принимаете отклик: {Answer.objects.get(id=id).text}'}
        return render(request, 'confirm_answer.html', context=to_html)

    def post(self, request, *args, **kwargs):
        id_ad = 0
        for pk, number in kwargs.items():
            id_ad = int(number)
        answer = Answer.objects.get(id = id_ad)
        answer.status = 'Принят'
        answer.save()
        user = request.POST['user']
        send_mail(
            'Ваш отклик приняли',
            f'{answer.user.username}, Пользователь:{user} принял ваш отклик на объявление: {answer.ad.header}. Вы можете связаться с ним по почте: {answer.ad.author.email}',
            'viktorsung@yandex.ru',
            [answer.user.email],
        )
        return redirect('answer_to_my_ad')


class DeleteAnswer(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # получаю ид объявления на которое отвечают
        id = 0
        for pk, number in kwargs.items():
            id = int(number)
        to_html = {'text': f'Вы удаляете отклик: {Answer.objects.get(id=id).text}'}
        return render(request, 'delete_answer.html', context=to_html)

    def post(self, request, *args, **kwargs):
        id_ad = 0
        for pk, number in kwargs.items():
            id_ad = int(number)
        answer = Answer.objects.get(id = id_ad)
        answer.status = 'Удален'
        answer.save()
        user = request.POST['user']
        send_mail(
            'Ваш отклик отклонили',
            f'{answer.user.username}, Пользователь:{user} отклонил ваш отклик на объявление: {answer.ad.header}',
            'viktorsung@yandex.ru',
            [answer.user.email],
        )
        return redirect('answer_to_my_ad')


class CreateAd(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        to_html = {'categories': categories,
                   'update': 'no'}
        return render(request, 'create_ad.html', context=to_html)

    def post(self, request, *args, **kwargs):
        user_from = request.POST['user']
        user_from = User.objects.get(username=f'{user_from}')
        category = request.POST['category1']
        category = Category.objects.get(name=category)
        header = request.POST['header']
        text = request.POST['text']
        fs = FileSystemStorage()

        try:
            image1 = request.FILES['image1']
            filename = fs.save(image1.name, image1)
        except:
            image1 = ''

        try:
            image2 = request.FILES['image2']
            filename = fs.save(image2.name, image2)
        except:
            image2 = ''

        new_ad = Ad(
            author=user_from,
            category=category,
            header=header,
            text=text,
            image1=image1,
            image2=image2,
        )
        new_ad.save()
        return redirect('ad_list')


class UpdateAd(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        id = 0
        for pk, number in kwargs.items():
            id = int(number)
        ad_upd = Ad.objects.get(id=id)
        to_html = {'categories': categories,
                   'update': 'yes',
                   'ad_upd': ad_upd}
        return render(request, 'create_ad.html', context=to_html)

    def post(self, request, *args, **kwargs):
        if request.POST['updated'] == 'yes':

            id_ad = 0
            for pk, number in kwargs.items():
                id_ad = int(number)
            ad = Ad.objects.get(id = id_ad)
            category = request.POST['category1']
            ad.category = Category.objects.get(name=category)
            ad.header = request.POST['header']
            ad.text = request.POST['text']
            fs = FileSystemStorage()
            try:
                image1 = request.FILES['image1']
                filename = fs.save(image1.name, image1)
                ad.image1 = image1
            except:
                ad.image1 = ''

            try:
                image2 = request.FILES['image2']
                filename = fs.save(image2.name, image2)
                ad.image2 = image2
            except:
                ad.image2 = ''

            ad.save()
        return redirect('ad_list')