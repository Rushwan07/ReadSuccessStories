from django.contrib import admin

# Register your models here.
from .models import Post, Viewers

admin.site.register(Post)
admin.site.register(Viewers)