from rest_framework import generics
from rest_framework import permissions
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models.functions import Trunc
from django.contrib.auth.models import User

from posts.models import Post, PostLike
from posts.serializers import PostSerializer, PostLikeSerializer
from posts.permissions import IsOwnerOrReadOnly
from posts.helper import get_request_data


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class PostLikeView(generics.ListCreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        like = PostLike.objects.filter(post=post, user=self.request.user).first()
        if not like:
            serializer.save(user=self.request.user, post=post)
        else:
            like.delete()


def likes_stats(request):
    data = get_request_data(request)
    likes = PostLike.objects.filter(date_created__range=[data['date_from'], data['date_to']])
    result = likes.annotate(datetime=Trunc('date_created', 'day')).values('datetime').annotate(num=Count('id'))
    return JsonResponse(list(result), safe=False)


def user_stats(request):
    data = User.objects.all().values('id', 'username', 'profile__last_activity')
    return JsonResponse(list(data), safe=False)
