from django.db import migrations

"""Due to optimization trigram similarity on basic for field
https://www.postgresql.org/docs/9.6/pgtrgm.html
https://www.postgresqltutorial.com/postgresql-indexes/postgresql-drop-index/

For create automatically in future we can use the solution is mentioned here:
https://stackoverflow.com/questions/44820345/creating-a-gin-index-with-trigram-gin-trgm-ops-in-django-model
"""


class Migration(migrations.Migration):

    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('account', '0062_auto_20200728_0837'),
    ]

    migration = '''
        CREATE INDEX IF NOT EXISTS account_university_name_trgm_idx ON account_university USING GIST (name gist_trgm_ops);
    '''

    reverse_migration = '''
        DROP INDEX IF EXISTS account_university_name_trgm_idx CASCADE;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
