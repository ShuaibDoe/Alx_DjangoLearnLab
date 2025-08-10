from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="John Doe")

    def test_str_representation(self):
        self.assertEqual(str(self.author), "John Doe")


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jane Smith")
        self.book = Book.objects.create(
            title="Test Book",
            description="Test description",
            author=self.author
        )

    def test_str_representation(self):
        self.assertEqual(str(self.book), "Test Book")


class SerializerTest(TestCase):
    def test_author_serializer(self):
        author = Author.objects.create(name="Serialized Author")
        serializer = AuthorSerializer(author)
        self.assertEqual(serializer.data["name"], "Serialized Author")

    def test_book_serializer(self):
        author = Author.objects.create(name="Serialized Author")
        book = Book.objects.create(
            title="Serialized Book",
            description="Some description",
            author=author
        )
        serializer = BookSerializer(book)
        self.assertEqual(serializer.data["title"], "Serialized Book")
        self.assertEqual(serializer.data["author"], author.id)


class ViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Author A")
        self.book1 = Book.objects.create(
            title="Alpha Book",
            description="First description",
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Beta Book",
            description="Second description",
            author=self.author
        )

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # assuming pagination

    def test_filter_books_by_title(self):
        url = reverse("book-list")
        response = self.client.get(url, {"search": "Alpha"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Alpha Book")

    def test_order_books_by_title(self):
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "title"})
        titles = [b["title"] for b in response.data["results"]]
        self.assertEqual(titles, sorted(titles))
