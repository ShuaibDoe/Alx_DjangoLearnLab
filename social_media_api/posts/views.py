from rest_framework import viewsets, permissions, mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # POST /posts/{id}/like/
    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({"detail": "Already liked."}, status=400)
        # Notify post author (if needed, via notifications app signal or direct create)
        return Response({"detail": "Post liked."}, status=201)

    # POST /posts/{id}/unlike/
    @action(detail=True, methods=["post"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        Like.objects.filter(post=post, user=request.user).delete()
        return Response({"detail": "Post unliked."})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("post", "author").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(APIView):
    """
    Returns posts from users the current user follows, newest first.
    """
    def get(self, request):
        user = request.user
        following_ids = user.following.values_list("id", flat=True)
        qs = Post.objects.filter(author_id__in=following_ids).order_by("-created_at")
        page = self.request.query_params.get("page")
        # Use DRF paginator already configured
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginated = paginator.paginate_queryset(qs, request, view=self)
        serializer = PostSerializer(paginated, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)
