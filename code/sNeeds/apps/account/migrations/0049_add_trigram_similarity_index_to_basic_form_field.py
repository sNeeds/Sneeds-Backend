from django.db import migrations

"""Due to optimization trigram similarity on basic for field
https://www.postgresql.org/docs/9.1/sql-createindex.html
https://www.postgresqltutorial.com/postgresql-indexes/postgresql-drop-index/
"""


class Migration(migrations.Migration):

    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('account', '0048_add_similarity_to_pg'),
    ]

    migration = '''
        CREATE INDEX IF NOT EXISTS trgm_idx ON account_basicformfield USING GIST (name gist_trgm_ops);
    '''

    reverse_migration = '''
        DROP INDEX IF EXISTS trgm_idx CASCADE;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
