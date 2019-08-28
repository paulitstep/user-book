from django.urls import path

from .views import UserListView, UserDetailView, BookEditView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('book/<int:pk>/', BookEditView.as_view(), name='book_edit'),
]
