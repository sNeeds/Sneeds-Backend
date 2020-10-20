from rest_framework import  permissions

from . import models
from . import serializers

from abroadin.base.api import generics
from abroadin.apps.users.consultants.models import ConsultantProfile
from .permissions import UserFileOwnerPermission


class UserFileListView(generics.CListCreateAPIView):
    queryset = models.UserFile.objects.all()
    serializer_class = serializers.UserFileSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filterset_fields = ('user', 'type',)

    def get_queryset(self):
        user = self.request.user
        consultant_profile_qs = ConsultantProfile.objects.filter(user=user)
        if consultant_profile_qs.exists():
            return models.UserFile.objects.get_consultant_accessed_files(consultant_profile_qs.first())
        else:
            return models.UserFile.objects.filter(user=user)


class UserFileDetailView(generics.CRetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = models.UserFile.objects.all()
    serializer_class = serializers.UserFileSerializer
    permission_classes = [UserFileOwnerPermission, permissions.IsAuthenticated, ]
