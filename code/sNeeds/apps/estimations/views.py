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

from sNeeds.apps.account.models import University, FieldOfStudy, FieldOfStudyType, StudentDetailedInfo, \
    UniversityThrough


class ListUsersAutoFixture(autofixture.AutoFixture):
    class Values:
        age = staticmethod(
            lambda: None if random.randint(1, 3) < 2 else random.randint(16, 40)
        )
        is_married = staticmethod(
            lambda: None if random.randint(1, 3) < 2 else random.randint(0, 1)
        )



class ListUsers(APIView):
    @transaction.atomic
    def get(self, request, format=None):
        UniversityThrough.objects.all().delete()
        StudentDetailedInfo.objects.all().delete()

        ListUsersAutoFixture(StudentDetailedInfo).create(100)
        ListUsersAutoFixture(UniversityThrough).create(250)
