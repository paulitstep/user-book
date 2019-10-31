from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from .models import Book
from .views import UserDetailView, BookUpdateView


class BookModelTests(TestCase):

    def setUp(self):
        Book.objects.create(title='Test title', author='Test author', published_year=2019)

    def create_book(self, title='Test title'):
        return Book.objects.create(title=title)

    def test_book_create(self):
        obj = Book.objects.get(pk=1)
        self.assertEqual(obj.title, 'Test title')
        self.assertTrue(obj.author != '')

    def test_book_qs(self):
        title1 = 'A new title'
        self.create_book(title=title1)
        self.create_book(title=title1)
        self.create_book(title=title1)
        qs = Book.objects.filter(title=title1)
        self.assertEqual(qs.count(), 3)


class UsersListViewTests(TestCase):

    def test_user_creation(self):
        data = {
            'username': 'TestUser'
        }
        response = self.client.post(reverse('user_book:users-list'), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'TestUser')


class UserDetailViewTests(TestCase):

    def test_book_creation(self):
        test_user = User.objects.create_user(username='TestUser')

        self.assertEqual(User.objects.count(), 1)

        url = reverse('user_book:user-detail', kwargs={'username': test_user.username})

        with open('user_book/test_image.jpg', 'rb') as img:
            data = {
                'image': img,
                'title': 'Python/Django навсегда!',
                'author': 'Programmer',
                'published_year': 2019
            }
            response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_user.books.count(), 1)

        book = test_user.books.first()
        self.assertEqual(book.title, 'Python/Django навсегда!')


class BookUpdateViewTests(TestCase):

    def test_update_book(self):
        test_user = User.objects.create_user(username='TestUser')

        self.assertEqual(test_user, User.objects.get(id=test_user.id))

        reverse('user_book:user-detail', kwargs={'username': test_user.username})

        with open('user_book/test_image.jpg', 'rb') as img:
            book = Book(
                user=test_user,
                title='Python/Django навсегда!',
                author='Programmer',
                published_year=2019
            )
            book.image.save('image_name', img)
            book.save()
            test_user.books.add(book)

        self.assertEqual(test_user.books.all().count(), 1)
        book = test_user.books.first()

        url = reverse('user_book:book-update', kwargs={'pk': book.pk})

        self.assertEqual(url, f'/book/{book.pk}/')

        with open('user_book/test_image.jpg', 'rb') as file:
            new_data = {
                'user': test_user.pk,
                'image': file,
                'title': 'Testing is cool!',
                'author': 'TestLab',
                'published_year': 2018,
            }
            response = self.client.post(url, new_data)

        self.assertEqual(response.status_code, 302)

        book.refresh_from_db()

        self.assertEqual(book.title, 'Testing is cool!')
        self.assertEqual(book.author, 'TestLab')


class BookUpdateViewAdvanceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='New User')

    def test_user_auth(self):
        obj = Book.objects.create(title='A new book', author='A new author', published_year=2019)
        url = reverse('user_book:book-update', kwargs={'pk': obj.pk})
        request = self.factory.get(url)
        request.user = self.user

        response = BookUpdateView.as_view()(request, pk=obj.pk)

        self.assertEqual(response.status_code, 200)

    def test_user_get(self):
        url = reverse('user_book:user-detail', kwargs={'username': self.user.username})
        request = self.factory.get(url)
        request.user = self.user

        response = UserDetailView.as_view()(request, username=self.user.username)

        self.assertEqual(response.status_code, 200)

    def test_unauth_user(self):
        obj = Book.objects.create(title='A new book', author='A new author', published_year=2019)
        url = reverse('user_book:book-update', kwargs={'pk': obj.pk})
        request = self.factory.get(url)
        request.user = AnonymousUser()

        response = BookUpdateView.as_view()(request, pk=obj.pk)

        self.assertEqual(response.status_code, 200)
