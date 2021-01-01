from django.db import migrations, models
import django.db.models.deletion

CACHED_APPLYDATA_SEMESTER_YEARS = {

}

def _get_new_semester_years(apps, schema_editor, old_ones:iter):
    ApplyDataSemesterYear = apps.get_model("applydata", "semesteryear")
    new_ones = []
    for old_one in old_ones:
        identifier = str(old_one.year)+'_||_'+old_one.semester
        if identifier not in CACHED_APPLYDATA_SEMESTER_YEARS:
            obj = ApplyDataSemesterYear.objects.get(semester=old_one.semester, year=old_one.year)
            CACHED_APPLYDATA_SEMESTER_YEARS[identifier] = obj
        new_ones.append(CACHED_APPLYDATA_SEMESTER_YEARS[identifier])


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    FormWantToApply = apps.get_model("form", "wanttoapply")
    FormWantToApplyTransferSemesterGrade = apps.get_model("form", "wanttoapplytransfersemestergrade")
    for obj in FormWantToApply.objects.all():
        mid_obj = FormWantToApplyTransferSemesterGrade.objects.create(
            want_to_apply=obj,
        )
        mid_obj.form_semester_years.set([obj.semester_years])
        mid_obj.form_grades.set([obj.grades])


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('form', '0019_create_temp_wanttoapplytransfer'),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_func,
        ),
    ]