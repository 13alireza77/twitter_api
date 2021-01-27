from django.db.models import Q
from django.http import JsonResponse, Http404
from rest_framework import generics, permissions, filters
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins

from prof.models import Follow
from twitt.api.serializers import TwittCreateSerializer, TwittDeleteSerializer, ReTwittCreateSerializer, \
    TwittSerializer, UersLikeSerializer, CreateLikeSerializer, CommentCreateSerializer, HashtagSerializer
from twitt.models import Twitt, Retwitt, Like, Hashtag
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


class Twitt_create_view(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TwittCreateSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.twitt(self.request.user)
            if res:
                return JsonResponse({
                    'status': res,
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
        obs = Follow.objects.filter(user=user)
        al = [o.target.pk for o in obs]
        return Twitt.objects.filter(user__id__in=al)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TwittProfile_view(mixins.ListModelMixin, generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = TwittSerializer
    # queryset = Follow.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        # user = self.request.user
        obs = Follow.objects.filter(user__username=self.kwargs['username'])
        al = [o.target.pk for o in obs]
        return Twitt.objects.filter(user__id__in=al)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Like_create_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateLikeSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.like(self.request.user)
            if res:
                return JsonResponse({
                    'status': res,
                })
            else:
                return JsonResponse({
                    'status': False,
                })


class Likes_view(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UersLikeSerializer
    # queryset = Follow.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        return Like.objects.filter(twitt_id=self.request.data['pk'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Comment_create_view(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.comment(self.request.user)
            if res:
                return JsonResponse({
                    'status': res,
                })
            else:
                return JsonResponse({
                    'status': False,
                })


class Get_twitt(APIView):
    permission_classes = [IsAuthenticated]

    # serializer_class = UersLikeSerializer
    # queryset = Follow.objects.all()
    def get_object(self, pk):
        try:
            return Twitt.objects.filter(pk=pk).first()
        except Twitt.DoesNotExist:
            raise Http404

    # def get_queryset(self):
    #     return Twitt.objects.filter(twitt_id=self.request.data['pk']).first()

    def get(self, request, pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = TwittSerializer(snippet)
        return Response(serializer.data)


class Get_top_Hashtags(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['occurrences']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Event_view(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TwittSerializer
    # queryset = Follow.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        user = self.request.user
        obs = Follow.objects.filter(target=user).select_related('user').values_list('id', flat=True)
        return Twitt.objects.filter(id__in=obs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
