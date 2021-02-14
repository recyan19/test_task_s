from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views


urlpatterns = [
    path('posts/', views.PostListView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('posts/<int:pk>/like/', views.PostLikeView.as_view()),
    path('analytics/', views.likes_stats),
    path('users-stats/', views.user_stats),
]

urlpatterns = format_suffix_patterns(urlpatterns)
