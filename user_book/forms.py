from django import forms
from django.contrib.auth.models import User

from .models import Book

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class BookCreateForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['image', 'title', 'author', 'published_year']

    def clean(self):
        self.cleaned_data = super().clean()
        is_same_book_exists = Book.objects.filter(user=self.instance.user,
                                                  title=self.cleaned_data['title'],
                                                  author=self.cleaned_data['author'],
                                                  published_year=self.cleaned_data['published_year'])
        if is_same_book_exists:
            raise forms.ValidationError('У данного пользователя уже есть эта книга!')

