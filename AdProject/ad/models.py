from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.core.mail import send_mail
from ckeditor.fields import RichTextField


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    header = models.TextField()
    text = models.TextField()
    image1 = models.ImageField(blank=True)
    image2 = models.ImageField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length= 100, unique=True)


class Answer(models.Model):
    #кто откликается
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # на что откликается
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)
    text = models.TextField()
    status = models.TextField(default='На рассмотрении')
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('answer', args=[str(self.id)])

    # def status_confirm(self):
    #     self.status = 'Принят'
    #     send_mail(
    #         'Ваш отклие приняли',
    #         f'{self.user.username}, Пользователь:{self.ad.author.username} принял ваш отклик на объявление: {self.ad.header}. Вы можете связаться с ним по почте: {self.ad.author.email}',
    #         'viktorsung@yandex.ru',
    #         [self.user.email],
    #     )
    #     self.save()
    #     return redirect('answer_to_my_ad')
    #
    #
    # def status_delete(self):
    #     self.status = 'Удален'
    #     self.save()

