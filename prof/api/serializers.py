from rest_framework import serializers
from prof.models import UserProfile, Follow
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(validated_data['email'], password=validated_data['password'],
                                        username=validated_data['username'])
        return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'is_active', 'create_at', 'last_modif']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'target')
