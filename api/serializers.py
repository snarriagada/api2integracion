from rest_framework import serializers
from .models import Artist, Album, Track


class ArtistSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200)
    age = serializers.IntegerField()
    #albums = serializers.URLField(max_length=200)
    #tracks = serializers.URLField(max_length=200)



class AlbumSerializer(serializers.Serializer):

    #artist_id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    genre = serializers.CharField(max_length=200)
    #artist = serializers.URLField(max_length=200)
    #tracks = serializers.URLField(max_length=200)


class TrackSerializer(serializers.Serializer):

    #artist_id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    duration = serializers.FloatField(default=0)
    #artist = serializers.URLField(max_length=200)
    #tracks = serializers.URLField(max_length=200)