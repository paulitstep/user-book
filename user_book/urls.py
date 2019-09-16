from django.urls import path

from .views import UsersListView, UserDetailView, BookUpdateView

urlpatterns = [
    path('', UsersListView.as_view(), name='users-list'),
    path('user/<username>/', UserDetailView.as_view(), name='user-detail'),
    path('book/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
]
