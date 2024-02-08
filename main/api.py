from django.contrib.auth.models import User
from rest_framework import viewsets
from main.permission import UserViewsetPermission
from main.serializers import (
    UserCreateSerializer,
    UserInfoSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created, viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [UserViewsetPermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ["create"]:
            serializer_class = UserCreateSerializer

        return serializer_class

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data.get("password"))
        user.save()
