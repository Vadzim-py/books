from unittest import TestCase
from django.contrib.auth.models import User
from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        author_1 = User.objects.create_user(username='Author 1', first_name='A', last_name='B')
        author_2 = User.objects.create_user(username='Author 2', first_name='C', last_name='D')
        author_3 = User.objects.create_user(username='Author 3', first_name='E', last_name='F')

        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1', owner=author_1)

        UserBookRelation.objects.create(user=author_1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=author_2, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=author_3, book=self.book_1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))
