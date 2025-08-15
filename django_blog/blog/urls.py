from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import (RegisterView, profile_update, PostListView, PostDetailView, PostCreateView, PostUpdateView,
                    PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView, PostByTagListView, search, home)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', profile_update, name='profile'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='tagged_posts_list'),
    path('search/', search, name='search'),
    path('', home, name='home')

]