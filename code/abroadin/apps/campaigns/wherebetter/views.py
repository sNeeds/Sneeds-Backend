from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from abroadin.base.api import generics
from .models import AppliedRedeemCode, InviteInfo, Participant
from .permissions import IsParticipantOwner, URLUserMatchReqUser

from .serializers import (AppliedRedeemCodesRequestSerializer, AppliedRedeemCodesSerializer,
                          InviteInfoSerializer, InviteInfoRequestSerializer, SafeParticipantSerializer,
                          ParticipantRequestSerializer, ParticipantSerializer)


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


class ParticipantsAPIView(generics.CListCreateAPIView):
    queryset = Participant.objects.all().order_by('rank')
    request_serializer_class = ParticipantRequestSerializer
    serializer_class = SafeParticipantSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallResultsSetPagination


class ParticipantAPIView(generics.CRetrieveAPIView):
    lookup_field = 'user'
    lookup_url_kwarg = 'user_id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated, IsParticipantOwner]


class ApplyRedeemCodeAPIView(generics.CListCreateAPIView):
    lookup_field = 'participant__user'
    lookup_url_kwarg = 'user_id'
    queryset = AppliedRedeemCode.objects.all()
    request_serializer_class = AppliedRedeemCodesRequestSerializer
    serializer_class = AppliedRedeemCodesSerializer
    permission_classes = [IsAuthenticated, URLUserMatchReqUser]

    # def get_queryset(self):
    #     return AppliedRedeemCode.objects.filter(participant__user=self.request.user)


class InviteByReferralAPIView(generics.CListCreateAPIView):
    lookup_field = 'invitor__user'
    lookup_url_kwarg = 'user_id'
    queryset = InviteInfo.objects.all()
    request_serializer_class = InviteInfoRequestSerializer
    serializer_class = InviteInfoSerializer
    permission_classes = [IsAuthenticated, URLUserMatchReqUser]

    # def get_queryset(self):
    #     return InviteInfo.objects.filter(invitor_user=self.request.user)
