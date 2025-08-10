from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author


# Create your tests here.

class BookAPITests(APITestCase):
    """
        Setting up all the information i need like creating a user,author ,book
        and creating the reverse urls for create , detail , update ,delete
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.author = Author.objects.create(name='Gamal')
        self.book = Book.objects.create(title='Test Book', publication_year=2020, author=self.author)
        self.create_url = reverse('books-create')
        self.detail_url = reverse('book-detail')
        self.update_url = reverse('books-update')
        self.delete_url = reverse('books-delete')

    """
        testing creating a book for authenticated users 
        starting by loggin in the user , having data of the book ,
        then creating the book using the response and post request
        asserting Equal for the status code = 201 that it worked
        assertiung equal that the book created title is equal to the same data i passed
    """
    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'title': 'New Test Book', 'publication_year': 2022, 'author': self.author.pk}
        response = self.client.post(self.create_url, data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Book.objects.get(pk=response.data['id']).title, 'New Test Book')

    """
        testing updating a book for authenticated users 
        starting by loggin in the user , having updated data of the book ,
        then updating the book using the response and patch request
        asserting Equal for the status code = 200 that it worked
        assertiung equal that the book updated title is equal to the same data i passed
    """
    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        update_date = {'id': self.book.pk, 'title': 'Updated Test Book'}
        response = self.client.patch(self.update_url, update_date)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.book.title, 'Updated Test Book')

    """
        testing deleting a book for authenticated users 
        starting by loggin in the user , getting the data id of the book i want to delete,
        then deleting the book using the response and delete request
        asserting Equal for the status code = 204 that it worked
    """
    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        delete_data = {'id': self.book.pk}
        response = self.client.delete(self.delete_url, delete_data)
        self.assertEquals(response.status_code, 204)

    """
        testing the permission of the detail view as i have set as authenticated or Read Only
        first assert Equal with a get request for unauthenticated user
        then assert Equal with a get request for the authenticated user after loggin in the user
    """
    def test_book_detail_view_permissions(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
