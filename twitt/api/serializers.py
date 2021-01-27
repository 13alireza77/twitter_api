from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.db.models import F
from prof.api.serializers import UserSerializer
from prof.models import Event
from twitt.models import Twitt, Retwitt, Like, Comment, Hashtag
import re


def extract_hashtags(text):
    regex = "#(\w+)"
    return re.findall(regex, text)


class TwittCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=250, allow_null=True)
    image = serializers.ImageField(allow_null=True)
    video = serializers.FileField(allow_null=True)

    def twitt(self, user):
        text = self.validated_data['text']
        image = self.validated_data['image']
        video = self.validated_data['video']
        if text or image or video:
            twitt = Twitt(
                user=user,
                text=text,
                image=image,
                video=video,
            )
            twitt.save()
            if text:
                for h in extract_hashtags(text):
                    obj, created = Hashtag.objects.get_or_create(name=h)
                    if obj:
                        obj.twitts.add(twitt)
                        Hashtag.objects.filter(name=h).update(occurrences=F('occurrences') + 1)
                        obj.save()
                    else:
                        created.twitts.add(twitt)
                        created.save()
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
            obj, created = Event.objects.get_or_create(user__id=twitt.user.pk)
            obj.update = True
            obj.save()
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
    image = serializers.ImageField(allow_null=True)
    video = serializers.FileField(allow_null=True)
    likes = SerializerMethodField(allow_null=True)
    comments = SerializerMethodField(allow_null=True)
    user = UserSerializer(read_only=True)
    id = SerializerMethodField()

    class Meta:
        model = Twitt
        fields = ('id', 'user', 'text', 'date', 'image', 'video', 'likes', 'comments')

    def get_likes(self, obj):
        return Like.objects.filter(twitt_id=obj.id).count()

    def get_comments(self, obj):
        return Comment.objects.filter(parent__id=obj.id).select_related('twitt').values_list('id', flat=True)

    def get_id(self, obj):
        return obj.pk


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
            obj, created = Event.objects.get_or_create(user__id=twitt.user.pk)
            obj.update = True
            obj.save()
            return like.pk
        else:
            return None


class UersLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('user', 'date')


class CommentCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=250, allow_null=True)
    image = serializers.ImageField(allow_null=True)
    video = serializers.FileField(allow_null=True)
    pk = serializers.IntegerField()

    def comment(self, user):
        text = self.validated_data['text']
        image = self.validated_data['image']
        video = self.validated_data['video']
        pk = self.validated_data['pk']
        if (text or image or video) and pk:
            twittp = Twitt.objects.filter(pk=pk).first()
            twitt = Twitt(
                user=user,
                text=text,
                image=image,
                video=video,
            )
            twitt.save()
            comment = Comment(parent=twittp, twitt=twitt)
            comment.save()
            return comment.pk
        else:
            return None


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('name', 'occurrences', 'lastupdate')
