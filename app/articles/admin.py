from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields=('id', 'created_date', 'updated_date')
    
admin.site.register(Article, ArticleAdmin)