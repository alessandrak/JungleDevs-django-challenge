from django.contrib import admin

from .models import Author


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields=('id', 'created_date', 'updated_date')
    
admin.site.register(Author, AuthorAdmin)