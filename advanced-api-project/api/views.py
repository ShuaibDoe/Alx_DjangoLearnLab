from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly
from rest_framework.throttling import UserRateThrottle


# -------------------------
# Author list & create view
# -------------------------
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['birth_year']
    search_fields = ['name']
    ordering_fields = ['birth_year', 'name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# -------------------------
# Book list & create view
# -------------------------

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['publication_year', 'title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# -------------------------
# Custom API view: Recent Books
# -------------------------
class RecentBooksRateThrottle(UserRateThrottle):
    rate = '5/min'

class RecentBooksListView(generics.ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['publication_year', 'title']
    pagination_class = CustomPageNumberPagination
    throttle_classes = [RecentBooksRateThrottle]

    def get_queryset(self):
        years = self.request.query_params.get('years', 5)  # default: last 5 years
        try:
            years = int(years)
        except ValueError:
            years = 5
        cutoff_year = datetime.now().year - years
        return Book.objects.filter(publication_year__gte=cutoff_year)
    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
