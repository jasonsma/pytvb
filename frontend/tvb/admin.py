from django.contrib import admin
from tvb.models import Forum81Item, ThreadItem

class Forum81ItemAdmin(admin.ModelAdmin):
    list_display = ('subscribe', 'title', 'author', 'datePosted', 'first_episode', 'last_episode')
    ordering = ['-datePosted']

# Register your models here.
admin.site.register(Forum81Item, Forum81ItemAdmin)
admin.site.register(ThreadItem)
