from django.urls import path
from .views import AuthorListCreateView, BookListCreateView, RecentBooksView, BookDetailView

urlpatterns = [
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/recent/', RecentBooksView.as_view(), name='recent-books'),
]
