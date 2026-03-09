from django.contrib import admin


from .models import *
class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'id', 'created_at')
    search_fields = ('id', 'category_name')
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)

