from django.shortcuts import render

from base.api.viewsets import CAPIView


class SimilarProfiles(CAPIView):

    def get(self, request, form_id):
