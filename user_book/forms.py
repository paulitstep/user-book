from django import forms

from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        labels = {'image': 'Изображение', 'title': 'Название', 'author_year': 'Автор, год издания'}
        fields = ['image', 'title', 'author_year']

