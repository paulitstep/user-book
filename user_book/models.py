from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    image = models.ImageField(upload_to='user_book/')
    title = models.CharField(max_length=100)
    author_year = models.CharField(max_length=250)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/book/{self.id}/'