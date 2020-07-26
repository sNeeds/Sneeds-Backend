import csv
import os
import random

import autofixture
from autofixture import generators

from django.db import transaction
from rest_framework import status, generics, mixins, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.apps.account.models import University, FieldOfStudy, FieldOfStudyType, StudentDetailedInfo


class ListUsersAutoFixture(autofixture.AutoFixture):
    class Values:
        age = staticmethod(
            lambda: None if random.randint(1, 3) < 2 else random.randint(16, 60)
        )


class ListUsers(APIView):
    @transaction.atomic
    def get(self, request, format=None):
        StudentDetailedInfo.objects.all().delete()
        student_detailed_infos = autofixture.create(
            'account.StudentDetailedInfo',
            10,
            field_values={'is_superuser': True}
        )
