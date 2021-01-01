from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0022_set_new_grade_and_semesteryear_to_related_objects'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WantToApplyTransferSemesterGrade'
        )
    ]