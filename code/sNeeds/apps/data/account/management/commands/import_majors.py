from django.core.management.base import BaseCommand
from django.db import transaction

from .majors.extractor import get_nodes
from ...models import Major


class Command(BaseCommand):
    help = 'Imports majors'

    imported_nodes = []

    @transaction.atomic
    def handle(self, *args, **kwargs):
        Major.objects.all().delete()

        for node in get_nodes():
            parent = None
            if node.parent:
                parent = self.find_django_parent(node.parent)
            major = Major.objects.create(
                name=node.content,
                search_name=node.content + " major field of study",
                parent_major=parent
            )
            self.imported_nodes.append((major, node))

    def find_django_parent(self, python_parent):
        for d_node, p_node in self.imported_nodes:
            if p_node is python_parent:
                return d_node
