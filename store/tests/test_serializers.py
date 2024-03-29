from django.db.models import Count, Case, When
from django.test import TestCase
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer
from django.contrib.auth import get_user_model


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        # Assuming User model has been imported and there is a user with username 'Author 1'
        users = get_user_model()
        author_1 = users.objects.create_user(username='Author 1', first_name='A', last_name='B')
        author_2 = users.objects.create_user(username='Author 2', first_name='C', last_name='D')
        author_3 = users.objects.create_user(username='Author 3', first_name='E', last_name='F')

        book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1', owner=author_1)
        book_2 = Book.objects.create(name='Test book 2', price=55, author_name='Author 2', owner=author_2)

        UserBookRelation.objects.create(user=author_1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=author_2, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=author_3, book=book_1, like=True, rate=4)

        UserBookRelation.objects.create(user=author_1, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=author_2, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=author_3, book=book_2, like=False)
        # The number of all units if user like is true
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')

        data = BookSerializer(books, many=True).data
        expected_data = [
            {   # inspection using data from the variable 1, 2
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',  # from serial converts this to a decimal
                'author_name': 'Author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'Author 1',
                'readers': [
                    {
                        'first_name': 'A',
                        'last_name': 'B'
                    },
                    {
                        'first_name': 'C',
                        'last_name': 'D'
                    },
                    {
                        'first_name': 'E',
                        'last_name': 'F'
                    },
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',  # decimal value
                'author_name': 'Author 2',
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': 'Author 2',
                'readers': [
                    {
                        'first_name': 'A',
                        'last_name': 'B'
                    },
                    {
                        'first_name': 'C',
                        'last_name': 'D'
                    },
                    {
                        'first_name': 'E',
                        'last_name': 'F'
                    },
                ]
            },
        ]
        self.assertEqual(expected_data, data)
