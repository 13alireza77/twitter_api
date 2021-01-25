from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, permissions, filters
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from twitt.api.serializers import TwittCreateSerializer, TwittDeleteSerializer, ReTwittCreateSerializer, TwittSerializer
from twitt.models import Twitt, Retwitt


class Twitt_create_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TwittCreateSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.twitt(self.request.user)
            if res:
                return JsonResponse({
                    'status': True,
                })
            else:
                return JsonResponse({
                    'status': False,
                })


class Twitt_delete_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TwittDeleteSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.remove()
            if res:
                return JsonResponse({
                    'status': True,
                })
            else:
                return JsonResponse({
                    'status': False,
                })


class ReTwitt_create_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReTwittCreateSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.retwitt(self.request.user)
            if res:
                return JsonResponse({
                    'status': True,
                })
            else:
                return JsonResponse({
                    'status': False,
                })


class Twitt_view(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TwittSerializer
    # queryset = Follow.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        user = self.request.user
        return Twitt.objects.filter(Q(user=user) | Q(retwitt__user=user))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# class Follower_view(mixins.ListModelMixin, generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = FollowerSerializer
#     queryset = Follow.objects.all()
#     filter_backends = [filters.OrderingFilter]
#     ordering = ['date']
#
#     # def get_queryset(self):
#     #     user = self.request.user
#     #     return Follow.objects.filter(target=user)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
