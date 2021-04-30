from django.core.management.base import BaseCommand
from django.db import transaction, connection, OperationalError
from django.conf import settings


def create_test_db():
    main_db_name = settings.DATABASES['default']['NAME']
    test_db_name = settings.DATABASES['custom_test_db']['NAME']

    with connection.cursor() as cursor:
        cursor.execute('DROP DATABASE IF EXISTS {} ;'.format(test_db_name))
        try:
            cursor.execute('CREATE DATABASE {} WITH TEMPLATE {};'.format(test_db_name, main_db_name))
        except OperationalError:
            cursor.execute(
                "SELECT pid, usename, client_addr FROM pg_stat_activity WHERE datname ='{}';".format(main_db_name))
            cursor.execute('CREATE DATABASE {} WITH TEMPLATE {};'.format(test_db_name, main_db_name))


class Command(BaseCommand):
    help = 'Create custom test data base from main database'

    def handle(self, *args, **kwargs):
        create_test_db()
