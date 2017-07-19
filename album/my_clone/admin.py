from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

