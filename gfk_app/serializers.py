from rest_framework import serializers
from .models import Album

class ViewCountSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)
    class Meta:
        model = Album
        fields = ['id', 'album_name', 'artist', 'tracks']

class AddAlbumSerializer(serializers.ModelSerializer):
    artist = serializers.CharField(max_length=10, min_length=3, required=True)
    album_name = serializers.CharField(max_length=10, min_length=3, required=False)
    class Meta:
        model = Album
        fields = ['id', 'album_name', 'artist']
