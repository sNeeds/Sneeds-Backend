from abroadin.apps.store.applyprofilestore.models import ApplyProfileGroup
from abroadin.apps.store.applyprofilestore.serializers import ApplyProfileGroupRequestSerializer, \
    ApplyProfileGroupSerializer
from abroadin.base.api.generics import CListCreateAPIView, CRetrieveUpdateDestroyAPIView


class ApplyProfileGroupListView(CListCreateAPIView):
    queryset = ApplyProfileGroup.objects.none()
    request_serializer_class = ApplyProfileGroupRequestSerializer
    serializer_class = ApplyProfileGroupSerializer
    permission_classes = []


class ApplyProfileGroupDetailView(CRetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = ApplyProfileGroup.objects.all()
    request_serializer_class = ApplyProfileGroupRequestSerializer
    serializer_class = ApplyProfileGroupSerializer
    permission_classes = []
