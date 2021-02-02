from rest_framework.permissions import IsAuthenticated

from abroadin.apps.store.applyprofilestore.models import ApplyProfileGroup, SoldApplyProfileGroup
from abroadin.apps.store.applyprofilestore.permissions import ApplyProfileGroupOwner, SoldApplyProfileGroupOwner
from abroadin.apps.store.applyprofilestore.serializers import ApplyProfileGroupSerializer, SoldApplyProfileGroupSerializer
from abroadin.base.api.generics import CListCreateAPIView, CRetrieveUpdateDestroyAPIView, CListAPIView, \
    CRetrieveAPIView, CRetrieveDestroyAPIView


class ApplyProfileGroupListView(CListCreateAPIView):
    queryset = ApplyProfileGroup.objects.none()
    serializer_class = ApplyProfileGroupSerializer
    permission_classes = [IsAuthenticated]


class ApplyProfileGroupDetailView(CRetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = ApplyProfileGroup.objects.all()
    serializer_class = ApplyProfileGroupSerializer
    permission_classes = [IsAuthenticated, ApplyProfileGroupOwner]


class SoldApplyProfileGroupListView(CListAPIView):
    queryset = SoldApplyProfileGroup.objects.none()
    serializer_class = SoldApplyProfileGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SoldApplyProfileGroup.objects.filter(sold_to=self.request.user)
        return SoldApplyProfileGroup.objects.none()


class SoldApplyProfileGroupDetailView(CRetrieveAPIView):
    lookup_field = 'id'
    queryset = SoldApplyProfileGroup.objects.all()
    serializer_class = SoldApplyProfileGroupSerializer
    permission_classes = [IsAuthenticated, SoldApplyProfileGroupOwner]
