import csv
import os
import random

import autofixture
from autofixture import generators

from django.db import transaction
from django.http import HttpRequest, HttpResponse, Http404
from rest_framework import status, generics, mixins, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.apps.account.models import University, FieldOfStudy, FieldOfStudyType, StudentDetailedInfo, \
    UniversityThrough, PaymentAffordability, WantToApply
from sNeeds.apps.estimations.reviews import StudentDetailedFormReview


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
        ListUsersAutoFixture(UniversityThrough).create(100)
        ListUsersAutoFixture(WantToApply, follow_m2m={'universities': (1, 10)}).create(100)
        ListUsersAutoFixture(WantToApply, follow_m2m={'universities': (0, 0)}).create(50)

        return HttpResponse()


class FormCommentsDetail(APIView):
    def get_form_obj(self, form_id):
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get(self, request, form_id, format=None):
        form = self.get_form_obj(form_id)
        review = StudentDetailedFormReview(form)
        return Response(review.review_all())


class FormCommentsList(APIView):
    def get(self, request, format=None):
        forms = StudentDetailedInfo.objects.filter(user=request.user)
        reviews = [StudentDetailedFormReview(form).review_all() for form in forms]
        return Response(reviews)
