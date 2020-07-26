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
    UniversityThrough, PaymentAffordability, WantToApply


class ListUsersAutoFixture(autofixture.AutoFixture):
    class Values:
        age = staticmethod(
            lambda: None if random.randint(1, 3) < 2 else random.randint(16, 40)
        )
        is_married = staticmethod(
            lambda: None if random.randint(1, 3) < 2 else random.randint(0, 1)
        )
        graduate_in = staticmethod(
            lambda: random.randint(2000, 2030)
        )
        gpa = staticmethod(
            lambda: random.randint(10, 20)
        )
        prefers_full_fund = staticmethod(
            lambda: None if random.randint(1, 5) < 2 else random.randint(0, 1)
        )
        prefers_half_fund = staticmethod(
            lambda: None if random.randint(1, 5) < 2 else random.randint(0, 1)
        )
        prefers_self_fund = staticmethod(
            lambda: None if random.randint(1, 5) < 2 else random.randint(0, 1)
        )
        related_work_experience = staticmethod(
            lambda: None if random.randint(1, 5) > 2 else random.randint(1, 50)
        )


class ListUsers(APIView):
    @transaction.atomic
    def get(self, request, format=None):
        UniversityThrough.objects.all().delete()
        StudentDetailedInfo.objects.all().delete()
        WantToApply.objects.all().delete()

        ListUsersAutoFixture(StudentDetailedInfo).create(100)
        ListUsersAutoFixture(UniversityThrough).create(250)
        ListUsersAutoFixture(WantToApply).create(200)
