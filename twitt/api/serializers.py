from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from prof.api.serializers import UserSerializer
from prof.models import UserProfile, Follow
from django.contrib.auth import get_user_model

from twitt.models import Twitt, Retwitt, Like


class TwittCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=250)

    def twitt(self, user):
        text = self.validated_data['text']
        if text:
            twitt = Twitt(
                user=user,
                text=text,
            )
            twitt.save()
            return twitt.pk
        else:
            return None


class ReTwittCreateSerializer(serializers.Serializer):
    pk = serializers.IntegerField(min_value=0)

    def retwitt(self, user):
        pk = self.validated_data['pk']
        twitt = Twitt.objects.filter(pk=pk).first()
        if twitt:
            retwitt = Retwitt(
                user=user,
                twitt=twitt,
            )
            retwitt.save()
            return twitt
        else:
            return None


class TwittDeleteSerializer(serializers.Serializer):
    pk = serializers.IntegerField(min_value=0)

    def remove(self):
        try:
            pk = self.validated_data['pk']
            twitt = Twitt.objects.filter(pk=pk).first()
            twitt.delete()
            return twitt
        except:
            return None


class TwittSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    video = serializers.FileField()
    likes = SerializerMethodField()

    class Meta:
        model = Twitt
        fields = ('text', 'date', 'image', 'video', 'likes')

    def get_likes(self, obj):
        return Like.objects.filter(twitt_id=obj.id).count()


class CreateLikeSerializer(serializers.Serializer):
    pk = serializers.IntegerField(min_value=0)

    def like(self, user):
        pk = self.validated_data['pk']
        twitt = Twitt.objects.filter(pk=pk).first()
        if twitt:
            like = Like(
                user=user,
                twitt=twitt,
            )
            like.save()
            return like.pk
        else:
            return None


class UersLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('user', 'date')
