from django.shortcuts import render
from constants.statics import SimpleViewSet
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer

class PostViewSet(SimpleViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    list_filtering = {"owners" : "owners__in"}


class CommentViewSet(SimpleViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    create_serializer_class = CommentCreateSerializer
    list_filtering = {"body" : "body__icontains"}
# Create your views here.
