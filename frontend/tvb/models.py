from django.db import models

# Create your models here.

class Forum81Item(models.Model):
    first_episode = models.IntegerField()
    last_episode = models.IntegerField()
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    datePosted = models.DateTimeField()
    url = models.URLField()
    subscribe = models.BooleanField(default=False)
    episodes_downloaded = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class ThreadItem(models.Model):
    forumItem = models.ForeignKey(Forum81Item)
    url = models.URLField()
    title = models.CharField(max_length=200)
    episode = models.IntegerField()
    torrent = models.CharField(max_length=1000)
    downloaded = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title
