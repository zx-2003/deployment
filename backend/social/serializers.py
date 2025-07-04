# we send python objects to frontend thru our api. Converts python objects to json and sends to frontend.
# also will return info based on request. can also convert json into python equivalent code.

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields are the fields we want to accept when we are accepting / returning a new user
        fields = ["id", "username", "password"]
        # we accept password when creating a user but not giving it when returning info about user
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()

    # new fields for like, basically to see if someone has liked a post and the like count
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "created_at", "author", 
                  "author_username", "image", "like_count", "is_liked", "rating", "location",]
        # we should be able to read who author is but shouldnt be able to write who author is. Author decided by backend
        extra_kwargs = {"author": {"read_only": True}}
    
    def get_author_username(self, obj):
        return obj.author.username
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False
