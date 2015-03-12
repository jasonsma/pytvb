from django.contrib import admin
from tvb.models import Forum81Item, ThreadItem

class Forum81ItemAdmin(admin.ModelAdmin):
    list_display = ('subscribe_link',
                    'title',
                    'author',
                    'first_episode',
                    'last_episode',
                    'episodes_downloaded',
                    'datePosted',)
    ordering = ['-datePosted']
    actions = None
    list_display_links = ['title']

    def subscribe_link(self, obj):
        if obj.subscribe:
            img = '<img src="/static/admin/img/icon-yes.gif" alt="True" />'
        else:
            img = '<img src="/static/admin/img/icon-no.gif" alt="False" />'
        ret = '<a href=/tvb/%d/>' % obj.id
        return ret + img + '</a>'
    subscribe_link.allow_tags = True
    subscribe_link.short_description = "subscribe"

# Register your models here.
admin.site.register(Forum81Item, Forum81ItemAdmin)
admin.site.register(ThreadItem)
