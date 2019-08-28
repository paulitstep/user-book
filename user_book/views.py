from django import views
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from .forms import BookForm
from .models import Book


class UserListView(views.View):
    template_name = 'user_book/user_list.html'

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {username} добавлен!')
            return redirect('/')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request):
        return render(request, self.template_name, {'users': User.objects.all(), 'form': UserCreationForm()})


class UserDetailView(views.View):
    template_name = 'user_book/user_detail.html'

    def post(self, request, pk):
        query = get_object_or_404(User, pk=pk)
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Вы добавили новую книгу!')
            return redirect('user_book:user_detail', query.pk)
        else:
            return render(request, self.template_name, {'user': query, 'form': form})

    def get(self, request, pk):
        query = get_object_or_404(User, pk=pk)
        return render(request, self.template_name, {'user': query, 'form': BookForm()})


class BookEditView(views.View):
    template_name = 'user_book/book_edit.html'

    def post(self, request, pk):
        query = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Книга отредактирована!')
            return redirect('user_book:book_edit', query.pk)
        else:
            return render(request, self.template_name, {'query': query, 'form': form})

    def get(self, request, pk):
        query = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=query)
        return render(request, self.template_name, {'query': query, 'form': form})