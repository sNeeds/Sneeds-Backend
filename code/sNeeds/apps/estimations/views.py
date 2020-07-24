import csv
import os

from django.db import transaction
from rest_framework import status, generics, mixins, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.apps.account.models import University


class ListUsers(APIView):
    @transaction.atomic
    def get(self, request, format=None):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estimations/universities.csv')

        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = University.objects.get_or_create(
                    name=row[0],
                    rank=int(row[1]),
                )
