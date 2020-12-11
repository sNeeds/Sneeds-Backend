from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
