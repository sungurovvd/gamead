from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    header = models.TextField()
    text = RichTextField()
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length= 100, unique=True)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

