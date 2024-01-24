import json

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BookSerializer
from django.contrib.auth.models import User


class BooksApiTestCase(APITestCase):
    def setUp(self):  # func is run every time before
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=55,
                                          author_name='Author 5')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55,
                                          author_name='Author 2')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 55})
        serializer_data = BookSerializer([self.book_2,
                                          self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BookSerializer([self.book_1,
                                          self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_myself(self):
        url = reverse('book-list')
        # This line is getting the URL for the book list view.
        # The `reverse` function is used to get the URL from the URL pattern name.
        response = self.client.get(url, data={'name': 'Test book 2'})
        # get coverage for name and variable setUp value from
        serializer_data = BookSerializer([self.book_2], many=True).data
        #  This line is serializing the book instance `self.book_2` using the
        #  `BookSerializer` and getting the serialized data.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #  This line is checking if the response status code is HTTP 200 OK.
        self.assertEqual(serializer_data, response.data)
        #  This line is checking if the serialized data matches the response data.

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
                "id": 5,
                "name": "Essence 5",
                "price": "150.00",
                "author_name": "Author 5"
                }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
                "name": self.book_1.name,
                "price": 575,
                "author_name": self.book_1.author_name
                }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book_1 = Book.objects.get(id=self.book_1.id) or:
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_delete_myself(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

