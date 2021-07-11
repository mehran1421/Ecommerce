from django.contrib import admin
from .models import Notice


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('email', 'status')


admin.site.register(Notice, NoticeAdmin)
