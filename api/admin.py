from django.contrib import admin
from .models import UserQuery

@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'user_query', 'ai_answer')
    search_fields = ('user_query', 'ai_answer')
    list_filter = ('date',)
