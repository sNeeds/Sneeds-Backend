from django.core.management.base import BaseCommand
from django.utils import timezone

from .extractor import get_nodes
from ...models import Major

class Command(BaseCommand):
    help = 'Imports majors'

    def handle(self, *args, **kwargs):
        for node in get_nodes():
            print(node)