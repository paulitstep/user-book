from django import views
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView
from django.views.generic.base import View

from .forms import UserCreationForm, BookCreateForm
from .models import Book

class UsersListView(FormView):
    model = User
    template_name = 'user_book/users_list.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('user_book:users-list')

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.filter(is_active=True)
        return super(UsersListView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Пользователь {username} добавлен!')
        return super().form_valid(form)


class UserDetailView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        book_creation_form = BookCreateForm()
        return render(request, 'user_book/user_detail.html', {'user': user,
                                                              'form': book_creation_form})

    def post(self, request, username):
        form = BookCreateForm(request.POST, request.FILES)
        user = User.objects.get(username=username)
        form.instance.user = user
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы добавили новую книгу!')
            return redirect('user_book:user-detail', user.username)
        else:
            return render(request, 'user_book/user_detail.html', {'user': user, 'form': form})

class BookUpdateView(UpdateView):
    model = Book
    template_name = 'user_book/book_update.html'
    fields = '__all__'
    context_object_name = 'book'
    success_url = reverse_lazy('user_book:users-list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Книга отредактирована!')
        return super().form_valid(form)


class BookEditView(views.View):
    template_name = 'user_book/book_edit.html'

    def post(self, request, pk):
        query = get_object_or_404(Book, pk=pk)
        form = BookCreateForm(request.POST, request.FILES, instance=query)
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
        form = BookCreateForm(instance=query)
        return render(request, self.template_name, {'query': query, 'form': form})