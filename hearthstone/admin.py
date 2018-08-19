from django.contrib import admin
from .models import Image, Voice, Comment
# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish')
    list_filter = ('created', 'publish', 'author')
    search_fields = ('title', 'description')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['publish']
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image)
admin.site.register(Voice)