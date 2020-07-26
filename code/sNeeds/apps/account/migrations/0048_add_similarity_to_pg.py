from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations

"""Before run migrate command enter this into postgres shell
CREATE EXTENSION pg_trgm;
"""

"""Due to activating trigram similarity in postgresql
https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/#trigramsimilarity
https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/operations/#trigramextension
"""


class Migration(migrations.Migration):

    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('account', '0047_create_name_text_search_trigger'),
    ]

    migration = '''
            CREATE EXTENSION IF NOT EXISTS pg_trgm;
        '''

    reverse_migration = '''
            DROP EXTENSION IF EXISTS pg_trgm;
        '''

    operations = [
        # NOTE: If permission denied error appeared use below sql
        # CREATE EXTENSION IF NOT EXISTS pg_trgm;
        # Or use this sql before migration
        # ALTER ROLE <user> SUPERUSER;
        migrations.RunSQL(migration, reverse_migration)
    ]
