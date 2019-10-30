from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Book(models.Model):
    user = models.ForeignKey(User,
                             related_name='books',
                             blank=True, null=True,
                             on_delete=models.SET_NULL,
                             verbose_name='Пользователь')
    image = models.ImageField(upload_to='books/%Y/%m/%d/', verbose_name='Обложка')
    title = models.CharField(max_length=100, verbose_name='Название')
    author = models.CharField(max_length=250, verbose_name='Автор')
    published_year = models.IntegerField(default=timezone.now().year, verbose_name='Год издания')
    created = models.DateField(auto_now_add=True, verbose_name='Дата создания записи')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/book/{self.id}/'
