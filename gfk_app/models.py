from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CommentModel(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='contentType')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.TextField()

class Post(models.Model):
    title = models.CharField(max_length=100)

class ImagePost(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField()

class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    def __str__(self):
        return '%d: %s' % (self.id, self.title)




