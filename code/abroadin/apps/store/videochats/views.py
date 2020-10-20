from rest_framework import  permissions
from rest_framework.response import Response

from abroadin.base.api import generics
from abroadin.apps.users.consultants.models import ConsultantProfile

from .models import Room
from .serializers import RoomSerializer
from .permissions import RoomOwnerPermission


class RoomListView(generics.CListAPIView):
    serializer_class = RoomSerializer
    filterset_fields = ('sold_time_slot',)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if ConsultantProfile.objects.filter(user=user).exists():
            # TODO: Order by start_time
            qs = Room.objects.filter(sold_time_slot__consultant__user=user).order_by("-created")
        else:
            qs = Room.objects.filter(sold_time_slot__sold_to=user).order_by("-created")
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Changed because previously one object was returned in a list
        if queryset.count() == 1 and self.request.GET.get("sold_time_slot") is not None:
            serializer = self.get_serializer(queryset.first())
        # For empty objects
        elif not queryset.exists() and self.request.GET.get("sold_time_slot") is not None:
            return Response({"detail": "Not found."}, status=404)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class RoomDetailAPIView(generics.CRetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, RoomOwnerPermission]
