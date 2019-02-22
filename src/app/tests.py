from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
from app.models import Book, Rate
from .factories import TokenFactory, UserFactory
from datetime import datetime

class BookCreateTests(APITestCase):
    def setUp(self):
        Book.objects.create(name='Book1', price=100, published_at=datetime(day=1, month=1, year=2019))
        self.book = Book.objects.get(name='Book1')
        
    def token_authorization(self):
        token = TokenFactory(user=UserFactory(is_active=True))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_list_book(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_detail_book(self):
        response = self.client.get(f'/books/{self.book.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Book1')

    def test_post_book(self):
        self.token_authorization()
        url = reverse('book-list')
        data = {'name': 'BookNew', 'price': 200, 'published_at': datetime(day=12, month=2, year=2019).strftime('%Y-%m-%dT%H:%M:%SZ')}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(name='BookNew')
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(book.name, 'BookNew')
        self.assertEqual(book.price, 200)
        self.assertEqual(book.published_at.strftime('%Y-%m-%dT%H:%M:%SZ'), datetime(day=12, month=2, year=2019).strftime('%Y-%m-%dT%H:%M:%SZ'))

    def test_patch_book(self):
        self.token_authorization()
        data = {'name': 'Book2', 'price': 500, 'published_at': datetime(day=30, month=4, year=2019).strftime('%Y-%m-%dT%H:%M:%SZ')}
        response = self.client.patch(f'/books/{self.book.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_put_book(self):
        self.token_authorization()
        data = {'name': 'Book3', 'price': 150, 'published_at': datetime(day=22, month=4, year=2019).strftime('%Y-%m-%dT%H:%M:%SZ')}
        response = self.client.put(f'/books/{self.book.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_delete_book(self):
        self.token_authorization()
        response = self.client.delete(f'/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_post_rate(self):
        data_post = {'value': 2}
        response = self.client.post(f'/books/{self.book.id}/rating/', data_post, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rate.objects.get().value, 2)
        self.assertEqual(Rate.objects.get().book.id, self.book.id)
