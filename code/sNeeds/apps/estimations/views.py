import csv
import os

from django.db import transaction
from rest_framework import status, generics, mixins, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.apps.account.models import University, FieldOfStudy, FieldOfStudyType


class ListUsers(APIView):
    @transaction.atomic
    def get(self, request, format=None):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estimations/fields.csv')

        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = FieldOfStudyType.objects.get_or_create(
                    name=row[1],
                )

        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = FieldOfStudy.objects.get_or_create(
                    major_type=FieldOfStudyType.objects.get(name=row[1]),
                    name=row[0],
                )
