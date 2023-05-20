from .models import Post, Comment
from rest_framework import serializers
from accounting.serializers import UserProfileSerializer
from accounting.views import UserProfileViewSet

class PostSerializer(serializers.ModelSerializer):
    owners = UserProfileSerializer(many=True)
    
    class Meta:
        model = Post
        fields = "__all__"
        depth = 3


class CommentSerializer(serializers.ModelSerializer):
    #owner = UserProfileSerializer()
    post = PostSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("body", "owner")

    
    