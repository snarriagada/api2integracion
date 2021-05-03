from django.db import models

# Create your models here.


class Artist(models.Model):
    id = models.CharField(max_length=70, primary_key=True)
    name = models.CharField(max_length=200,blank=False, default='')
    age = models.IntegerField(default=0)
    albums = models.URLField(max_length=200)
    tracks = models.URLField(max_length=200)
    self = models.URLField(max_length=200,default='')


class Album(models.Model):
    id = models.CharField(max_length=70, primary_key=True)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=False, default='')
    genre = models.CharField(max_length=200,blank=False, default='')
    artist = models.URLField(max_length=200)
    tracks = models.URLField(max_length=200)
    self = models.URLField(max_length=200,default='')


class Track(models.Model):
    id = models.CharField(max_length=70, primary_key=True)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=False, default='')
    duration = models.FloatField(max_length=200,blank=False)
    times_played = models.IntegerField(max_length=200,blank=False,default=0)
    artist = models.URLField(max_length=200)
    album = models.URLField(max_length=200)
    self = models.URLField(max_length=200,default='')
