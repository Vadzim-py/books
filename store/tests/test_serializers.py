from django.test import TestCase
from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        # Assuming User model has been imported and there is a user with username 'Author 1'
        from django.contrib.auth import get_user_model
        User = get_user_model()
        author_1 = User.objects.create_user(username='Author 1')
        author_2 = User.objects.create_user(username='Author 2')

        book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1', owner=author_1)
        book_2 = Book.objects.create(name='Test book 2', price=55, author_name='Author 2', owner=author_2)

        data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',  # Assuming the serializer converts this to a decimal
                'author_name': 'Author 1',
                'owner': author_1.id  # Assuming the serializer serializes the owner as the user id
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',  # Assuming the serializer converts this to a decimal
                'author_name': 'Author 2',
                'owner': author_2.id  # Assuming the serializer serializes the owner as the user id
            },
        ]
        self.assertEqual(expected_data, data)
