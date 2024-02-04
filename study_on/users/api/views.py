from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from study_on.services.permissions import IsAdminOrStuff
from study_on.users.api.serializers import ListUserSerializer, UserSerializer

User = get_user_model()


class UserFilter(filters.FilterSet):
    """Фильтр для пользователя"""

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """Пользователь"""

    serializer_class = ListUserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = (IsAdminOrStuff,)
    filterset_class = UserFilter
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]

    @action(detail=False, serializer_class=UserSerializer)
    def me(self, request):
        """Получить информацию о пользователе"""
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
