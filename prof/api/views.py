from itertools import chain

from django.http import JsonResponse, Http404
from django.utils import timezone
from rest_framework import generics, permissions, filters
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from prof.api.serializers import RegisterSerializer, UserSerializer, FollowCreateSerializer, FollowerSerializer, \
    FollowingSerializer, UnFollowSerializer, MySerializer, ChangePasswordSerializer, UpdateUserSerializer
from rest_framework import mixins
from prof.models import Follow, UserProfile, Event


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "status": True,
            })
        else:
            return JsonResponse({
                'status': False,
            })


class Logout_view(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return JsonResponse({
                'status': True,
                'detail': 'logout'
            })
        except Exception as e:
            return JsonResponse({
                'status': False,
                'detail': 'sth went wrong'})


class Follow_create_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FollowCreateSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.follow(self.request.user)
            if res:
                return JsonResponse({
                    'status': True,
                })
            else:
                return JsonResponse({
                    'status': False,
                })


class UnFollow_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UnFollowSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.unfollow(self.request.user)
            if res:
                return JsonResponse({
                    'status': True,
                })
            else:
                return JsonResponse({
                    'status': False,
                })


class Following_view(mixins.ListModelMixin, generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = FollowingSerializer
    # queryset = Follow.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        # user = self.request.user
        return Follow.objects.filter(user__username=self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Follower_view(mixins.ListModelMixin, generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer
    # queryset = Follow.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        # user = self.request.user
        return Follow.objects.filter(target__username=self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Get_Profie(APIView):
    # permission_classes = [IsAuthenticated]

    # serializer_class = UersLikeSerializer
    # queryset = Follow.objects.all()
    def get_object(self, username):
        try:
            return UserProfile.objects.filter(username=username).first()
        except UserProfile.DoesNotExist:
            raise Http404

    # def get_queryset(self):
    #     return Twitt.objects.filter(twitt_id=self.request.data['pk']).first()

    def get(self, request, username, *args, **kwargs):
        snippet = self.get_object(username)
        serializer = UserSerializer(snippet, context={'request': request})
        return Response(serializer.data)


class Get_My(APIView):
    permission_classes = [IsAuthenticated]

    # serializer_class = UersLikeSerializer
    # queryset = Follow.objects.all()
    def get_object(self, pk):
        try:
            return UserProfile.objects.filter(pk=pk.pk).first()
        except UserProfile.DoesNotExist:
            raise Http404

    # def get_queryset(self):
    #     return Twitt.objects.filter(twitt_id=self.request.data['pk']).first()

    def get(self, request, *args, **kwargs):
        snippet = self.get_object(request.user)
        serializer = MySerializer(snippet, context={'request': request})
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    parser_class = (FileUploadParser,)
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class GetEvent(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer
    # queryset = Follow.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        user = self.request.user
        try:
            e = Event.objects.filter(user__id=user).first()
            if e.update:
                d = e.date
                e.update = False
                objs = chain(UserProfile.objects.filter(like__twitt__user_id=user, like__date__gt=d),
                             UserProfile.objects.filter(retwitt__twitt__user__id=user, retwitt__date__gt=d),
                             UserProfile.objects.filter(follow__target__id=user, follow__date__gt=d))
                e.date = timezone.now
                e.save()
                return objs
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
