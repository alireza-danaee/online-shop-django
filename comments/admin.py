from django.contrib import admin
from .models import Comment




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'product', 'j_created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('user', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
