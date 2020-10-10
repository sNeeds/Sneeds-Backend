from rest_framework.permissions import IsAuthenticated

from sNeeds.base.api import generics
from . import serializers
from .models import BasicProduct, SoldBasicProduct, ClassProduct, SoldClassProduct, WebinarProduct, SoldWebinarProduct, \
    ClassRoomLink, WebinarRoomLink
from .permissions import SoldBasicProductOwnerPermission, IsLinkOwner


class BasicProductList(generics.CListAPIView):
    queryset = BasicProduct.objects.all()
    serializer_class = serializers.BasicProductSerializer


class BasicProductDetail(generics.CRetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = serializers.BasicProductSerializer
    queryset = BasicProduct.objects.all()


class ClassProductList(generics.CListAPIView):
    queryset = ClassProduct.objects.all()
    serializer_class = serializers.ClassProductSerializer
    ordering_fields = ['created']
    filterset_fields = ["is_held", "is_free"]
    search_fields = ['title', 'descriptions', 'headlines', 'lecturers']


class ClassProductDetail(generics.CRetrieveAPIView):
    lookup_field = 'slug'
    queryset = ClassProduct.objects.all()
    serializer_class = serializers.ClassProductSerializer


class WebinarProductList(generics.CListAPIView):
    queryset = WebinarProduct.objects.all()
    serializer_class = serializers.WebinarProductSerializer
    ordering_fields = ['created']
    filterset_fields = ["is_held", "is_free"]
    search_fields = ['title', 'descriptions', 'headlines', 'lecturers']


class WebinarProductDetail(generics.CRetrieveAPIView):
    lookup_field = 'slug'
    queryset = WebinarProduct.objects.all()
    serializer_class = serializers.WebinarProductSerializer


class SoldBasicProductList(generics.CListAPIView):
    queryset = SoldBasicProduct.objects.all()
    serializer_class = serializers.SoldBasicProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SoldBasicProduct.objects.filter(sold_to=user)


class SoldBasicProductDetail(generics.CRetrieveAPIView):
    lookup_field = 'id'
    serializer_class = serializers.SoldBasicProductSerializer
    queryset = SoldBasicProduct.objects.all()
    permission_classes = [IsAuthenticated, SoldBasicProductOwnerPermission]


class SoldClassProductList(generics.CListAPIView):
    queryset = SoldClassProduct.objects.all()
    serializer_class = serializers.SoldClassProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SoldClassProduct.objects.filter(sold_to=user)


class SoldClassProductDetail(generics.CRetrieveAPIView):
    lookup_field = 'id'
    queryset = SoldClassProduct.objects.all()
    serializer_class = serializers.SoldClassProductSerializer
    permission_classes = [IsAuthenticated, SoldBasicProductOwnerPermission]


class SoldWebinarProductList(generics.CListAPIView):
    queryset = SoldWebinarProduct.objects.all()
    serializer_class = serializers.SoldWebinarProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SoldWebinarProduct.objects.filter(sold_to=user)


class SoldWebinarProductDetail(generics.CRetrieveAPIView):
    lookup_field = 'id'
    queryset = SoldWebinarProduct.objects.all()
    serializer_class = serializers.SoldWebinarProductSerializer
    permission_classes = [IsAuthenticated, SoldBasicProductOwnerPermission]


class WebinarRoomLinkList(generics.CListAPIView):
    queryset = WebinarRoomLink.objects.all()
    serializer_class = serializers.WebinarRoomLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = WebinarRoomLink.objects.filter(user=user)
        return qs


class WebinarRoomLinkDetail(generics.CRetrieveAPIView):
    lookup_field = 'id'
    queryset = WebinarRoomLink.objects.all()
    serializer_class = serializers.WebinarRoomLinkSerializer
    permission_classes = [IsAuthenticated, IsLinkOwner]


class ClassRoomLinkList(generics.CListAPIView):
    queryset = ClassRoomLink.objects.all()
    serializer_class = serializers.ClassRoomLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = ClassRoomLink.objects.filter(user=user)
        return qs


class ClassRoomLinkDetail(generics.CRetrieveAPIView):
    lookup_field = 'id'
    queryset = ClassRoomLink.objects.all()
    serializer_class = serializers.ClassRoomLinkSerializer
    permission_classes = [IsAuthenticated, IsLinkOwner]



