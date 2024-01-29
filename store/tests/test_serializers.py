from django.test import TestCase
from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        # Assuming User model has been imported and there is a user with username 'Author 1'
        from django.contrib.auth import get_user_model
        users = get_user_model()
        author_1 = users.objects.create_user(username='Author 1')
        author_2 = users.objects.create_user(username='Author 2')

        book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1', owner=author_1)
        book_2 = Book.objects.create(name='Test book 2', price=55, author_name='Author 2', owner=author_2)

        data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {   # inspection using data from the variable 1, 2
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',  # from serial converts this to a decimal
                'author_name': 'Author 1',
                'owner': author_1.id  # Assuming the serializer serializes the owner as the user id
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',  # decimal value
                'author_name': 'Author 2',
                'owner': author_2.id
            },
        ]
        self.assertEqual(expected_data, data)
