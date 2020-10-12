from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from .extractor import get_nodes
from ...models import Major


class Command(BaseCommand):
    help = 'Imports majors'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        Major.objects.all().delete()
        #
        # for node in get_nodes():
        #     try:
        #         parent = Major.objects.get(name=node.parent)
        #     except Major.DoesNotExist:
        #         parent = None
        #
        #     Major.objects.create(
        #         name=node.content,
        #         search_name=node.content + "major field study of",
        #         major=parent
        #     )
