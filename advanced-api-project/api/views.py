from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework import filters
from .serializers import BookSerializer
from .models import Book


# Create your views here.


class BookListView(generics.ListAPIView):
    """
        Provides a read-only list of all books.
        * Only authenticated users are allowed to access this view or they will be allowed to READ it only.
        * Supports basic filtering based on title, publication year, and author.
        *Installed django-filter with pip install django-filter
        *added it in INSTALLED APPS and added the settings needed
        *imported DjangoFilterBackend
        *and added the fields i want to filter
        **Filtering**:
        - Enabled via DjangoFilterBackend.
        - Fields: `title`, `publication_year`, `author`
        - Example: `/api/books/?title=Python&publication_year=2021`

        **Searching**:
        - Enabled via SearchFilter.
        - Fields: `title`, `author__name` (author's name)
        - Example: `/api/books/?search=Python` searches in book titles and author names.

        **Ordering**:
        - Enabled via OrderingFilter.
        - Fields: `title`, `publication_year`
        - Example: `/api/books/?ordering=publication_year` for ascending order,
          `/api/books/?ordering=-publication_year` for descending order.


    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['title', 'publication_year']
    filterset_fields = ['title', 'publication_year', 'author']
    search_fields = ['title', 'author__name']


class BookDetailView(generics.RetrieveAPIView):
    """
        Provides a read-only list of a single book.
        * Only authenticated users are allowed to access this view or they will be allowed to READ it only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']


class BookCreateView(generics.CreateAPIView):
    """
        Provides a create API point for the Book.
        * Only authenticated users are allowed to access this view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
        Provides a Update API point for a single Book.
        * Only authenticated users are allowed to access this view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
        Provides a Delete API point for the Book.
        * Only authenticated users are allowed to access this view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
