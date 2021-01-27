from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.db.models import F
from prof.api.serializers import UserSerializer
from prof.models import Event, UserProfile
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
                print(text)
                for h in extract_hashtags(text):
                    obj, created = Hashtag.objects.get_or_create(name=h)
                    obj.twitts.add(twitt)
                    oc = obj.occurrences
                    obj.occurrences = oc + 1
                    obj.save()
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
            obj, created = Event.objects.get_or_create(user_id=twitt.user.pk)
            obj.update_retwitt = True
            obj.save()
            return twitt
        else:
            return None


class TwittDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)

    def remove(self):
        try:
            pk = self.validated_data['id']
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
    retwitts = SerializerMethodField(allow_null=True)
    user = UserSerializer(read_only=True)
    id = SerializerMethodField()

    class Meta:
        model = Twitt
        fields = ('id', 'user', 'text', 'date', 'image', 'video', 'likes', 'comments', 'retwitts')

    def get_likes(self, obj):
        obs = Like.objects.filter(twitt_id=obj.id)
        return [t.user.username for t in obs]

    def get_comments(self, obj):
        obs = Comment.objects.filter(parent__id=obj.id)
        return [t.twitt.id for t in obs]

    def get_retwitts(self, obj):
        obs = Retwitt.objects.filter(twitt_id=obj.id)
        return [t.user.username for t in obs]

    def get_id(self, obj):
        return obj.pk


class CreateLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)

    def like(self, user):
        pk = self.validated_data['id']
        twitt = Twitt.objects.filter(pk=pk).first()
        if twitt:
            like = Like(
                user=user,
                twitt=twitt,
            )
            like.save()
            obj, created = Event.objects.get_or_create(user_id=twitt.user.pk)
            obj.update_like = True
            obj.save()
            return like.pk
        else:
            return None


class DisLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    username = serializers.CharField(max_length=50)

    def dislike(self):
        id = self.validated_data['id']
        username = self.validated_data['username']
        print(id, username)
        try:
            if id and username:
                twitt = Twitt.objects.filter(pk=id).first()
                prof = UserProfile.objects.filter(username=username).first()
                like = Like.objects.filter(user=prof, twitt=twitt).first()
                like.delete()
                return 1
            else:
                return None
        except:
            return None


# class UersLikeSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Like
#         fields = ('user', 'date')


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
