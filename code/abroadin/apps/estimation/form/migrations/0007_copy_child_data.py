from django.conf import settings
import django.core.validators
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations, models
import django.db.models.deletion


def copy_sdi_to_sdi_base(apps, schema_editor):
    SDI = apps.get_model("form", "StudentDetailedInfo")
    SDIBase = apps.get_model("form", "StudentDetailedInfoBase")

    for obj in SDI.objects.all():
        base = obj.studentdetailedinfobase_ptr
        base.t_user = obj.user
        base.t_age = obj.age
        base.t_gender = obj.gender
        base.t_is_married = obj.is_married
        base.t_payment_affordability = obj.payment_affordability
        base.t_prefers_full_fund = obj.prefers_full_fund
        base.t_prefers_half_fund = obj.prefers_half_fund
        base.t_prefers_self_fund = obj.prefers_self_fund
        base.t_comment = obj.comment
        base.t_powerful_recommendation = obj.powerful_recommendation
        base.t_linkedin_url = obj.linkedin_url
        base.t_homepage_url = obj.homepage_url
        base.t_value = obj.value
        base.t_rank = obj.rank

        base.save()

    SDIBase.objects.all().exclude(id__in=SDI.objects.all()).delete()

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('form', '0006_auto_20210418_1207'),
    ]

    operations = [
        migrations.RunPython(
            code=copy_sdi_to_sdi_base, reverse_code=lambda *args: None
        ),
    ]
