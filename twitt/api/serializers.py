from rest_framework import serializers
from prof.models import UserProfile, Follow
from django.contrib.auth import get_user_model

from twitt.models import Twitt, Retwitt


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
            return twitt
        else:
            return None


class ReTwittCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=250)

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
    class Meta:
        model = Twitt
        fields = ('text', 'date')

# class FollowingSerializer(serializers.ModelSerializer):
#     target = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Follow
#         fields = ('target', 'date')
