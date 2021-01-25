from django.http import JsonResponse
from rest_framework import generics, permissions, filters
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from prof.api.serializers import RegisterSerializer, UserSerializer, FollowSerializer
from rest_framework import mixins

from prof.models import Follow


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "status": True,
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


class Follow_create_view(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Follow_delete_view(mixins.DestroyModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class Following_view(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(target=user).select_related('target')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Follower_view(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(target=user).select_related('target')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
