from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('form', '0020_store_wanttoapply_grade_and_semester_in_middle_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wanttoapply',
            name='grades',
        ),
        migrations.AddField(
            model_name='wanttoapply',
            name='grades',
            field=models.ManyToManyField(to='applydata.Grade'),
        ),

        migrations.RemoveField(
            model_name='wanttoapply',
            name='semester_years',
        ),
        migrations.AddField(
            model_name='wanttoapply',
            name='semester_years',
            field=models.ManyToManyField(to='applydata.SemesterYear'),
        ),
    ]