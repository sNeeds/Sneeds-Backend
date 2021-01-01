

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('account', '0024_delete_redundant_objects_with_applydata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentdetailedinfo',
            name='universities',
        ),
    ]