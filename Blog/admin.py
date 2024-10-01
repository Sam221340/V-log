from django.contrib import admin

# Register your models here.
from Blog.models import Post, Category, Tag

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
