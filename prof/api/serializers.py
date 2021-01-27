from django.contrib.auth.password_validation import validate_password
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
    picture_url = serializers.SerializerMethodField('get_picture_url')
    cover_url = serializers.SerializerMethodField('get_cover_url')

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'name', 'is_active', 'create_at', 'last_modif', 'picture_url', 'cover_url')

    def get_picture_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.picture_url)

    def get_cover_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.cover_url)


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
    picture_url = serializers.SerializerMethodField('get_picture_url')
    cover_url = serializers.SerializerMethodField('get_cover_url')
    retwittl = SerializerMethodField()
    likel = SerializerMethodField()
    followl = SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'name', 'is_active', 'create_at', 'last_modif', 'picture_url', 'cover_url',
                  'retwittl',
                  'likel', 'followl']

    def get_picture_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.picture_url)

    def get_cover_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.cover_url)

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_null=True)
    image = serializers.ImageField(allow_null=True)
    cover = serializers.ImageField(allow_null=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'name', 'email', 'image', 'cover')
        extra_kwargs = {
            'name': {'required': True}
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if UserProfile.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if UserProfile.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.first_name = validated_data['name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        if self.context['image']:
            instance.image = validated_data['image']
        if self.context['cover']:
            instance.cover = validated_data['cover']

        instance.save()

        return instance
