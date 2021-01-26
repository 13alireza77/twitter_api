from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from prof.models import UserProfile, Follow
from django.contrib.auth import get_user_model

from twitt.models import Retwitt, Like


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=False)

    class Meta:
        User = get_user_model()
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        User = get_user_model()
        try:
            user = User.objects.create_user(validated_data['email'], password=validated_data['password'],
                                            username=validated_data['username'])
        except:
            try:
                user = User.objects.create_user(validated_data['email'], password=validated_data['password'])
            except:
                return None
        return user


class UserSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()
    cover = serializers.ImageField()

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'name', 'is_active', 'create_at', 'last_modif', 'picture', 'cover']


class FollowCreateSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)

    def follow(self, user):
        email = self.validated_data['email']
        target = UserProfile.objects.filter(email=email).first()
        if user and target:
            follow = Follow(
                user=user,
                target=target,
            )
            follow.save()
            return follow
        return None


class UnFollowSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)

    def unfollow(self, user):
        email = self.validated_data['email']
        target = UserProfile.objects.filter(email=email).first()
        if user and target:
            follow = Follow.objects.filter(user=user, target=target).first()
            follow.delete()
            return follow
        return None


class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'date')


class FollowingSerializer(serializers.ModelSerializer):
    target = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('target', 'date')


# class LogSerializer(serializers.ModelSerializer):
#     retwittl = serializers.RelatedField(source='retwitt', read_only=True)
#     likel = serializers.RelatedField(source='like', read_only=True)
#     followl = serializers.RelatedField(source='follow', read_only=True)
#
#     class Meta:
#         model = Log
#         fields = ('user', 'retwittl', 'likel')


class MySerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()
    cover = serializers.ImageField()
    retwittl = SerializerMethodField()
    likel = SerializerMethodField()
    followl = SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'name', 'is_active', 'create_at', 'last_modif', 'picture', 'cover', 'retwittl',
                  'likel', 'followl']

    def get_retwittl(self, obj):
        ob = Retwitt.objects.filter(user__id=obj.id)
        res = []
        lob = ob.select_related('target').values_list('id', flat=True)
        for i, j in zip(ob, lob):
            res.append((i.date, j))
        return res

    def get_likel(self, obj):
        ob = Like.objects.filter(user__id=obj.id)
        res = []
        lob = ob.select_related('target').values_list('id', flat=True)
        for i, j in zip(ob, lob):
            res.append((i.date, j))
        return res

    def get_followl(self, obj):
        ob = Follow.objects.filter(user__id=obj.id)
        res = []
        lob = ob.select_related('target').values_list('id', flat=True)
        for i, j in zip(ob, lob):
            res.append((i.date, j))
        return res
