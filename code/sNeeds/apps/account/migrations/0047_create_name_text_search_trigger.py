from django.db import migrations

"""Due to optimization full text search on basic for field
https://findwork.dev/blog/optimizing-postgres-full-text-search-in-django/
https://www.postgresql.org/docs/current/textsearch-features.html#TEXTSEARCH-UPDATE-TRIGGERS
https://stackoverflow.com/questions/59754209/django-db-utils-programmingerror-syntax-error-at-or-near-function
"""

class Migration(migrations.Migration):

    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('account', '0046_auto_20200724_2237'),
    ]

    migration = '''
        CREATE TRIGGER name_search_update BEFORE INSERT OR UPDATE
        ON account_basicformfield FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(name_search, 'pg_catalog.simple', name);

        -- Force triggers to run and populate the text_search column.
        UPDATE account_basicformfield set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER name_search_update ON account_basicformfield;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
