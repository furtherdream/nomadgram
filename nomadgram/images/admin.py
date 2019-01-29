from django.contrib import admin
# images 에 있는 models.py 를 불러온다.
from . import models

# Register your models here.
# 클래스를 만들건데 이 것이 어드민 패널에 어떻게 보일지를 결정

# 클릭스를 등록해야 되는데 데코레이터를 사용할거야 : @
# 클래스와 간격을 두면 에러가 발생함

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    list_display_links = (
        'location',
    )

    search_fields = (
        'location',
        'caption',
    )

    list_filter = (
        'location',
        'creator'
    )

    list_display = (
        'file',
        'location',
        'caption',
        'creator',
        'created_at',
        'updated_at',
    )

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = (
        'creator',
        'image',
        'created_at',
        'updated_at',
    )

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        'message',
        'creator',
        'image',
        'created_at',
        'updated_at',
    )
