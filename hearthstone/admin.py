from django.contrib import admin
from .models import Image
from .models import Voice

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish','version')
    list_filter = ('publish', 'author')
    search_fields = ('title', 'description')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['publish','version']
class VoiceAdmin(admin.ModelAdmin):
    ordering = ['-file_type']
admin.site.register(Image, ImageAdmin)
admin.site.register(Voice, VoiceAdmin)