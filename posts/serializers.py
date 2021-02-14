from rest_framework import serializers
from posts.models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    liked = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'created_by', 'liked', 'likes_count', 'date_created']
        read_only_fields = ['likes_count', 'date_created']

    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and PostLike.objects.filter(post=obj, user=user).exists():
            return True
        return False


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post']
