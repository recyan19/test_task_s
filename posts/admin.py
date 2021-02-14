from django.contrib import admin
from posts.models import Post, PostLike


class PostLikeInline(admin.TabularInline):
    readonly_fields = ['date_created']
    model = PostLike
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'title']
    list_display_links = list_display
    inlines = [PostLikeInline]
