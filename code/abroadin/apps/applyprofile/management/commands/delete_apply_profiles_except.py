from pprint import pprint
from openpyxl import load_workbook, Workbook
from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType

from ...models import ApplyProfile, Admission

from abroadin.apps.data.account.models import University, Country, Major
from abroadin.apps.data.applydata.models import Education, RegularLanguageCertificate, Grade, LanguageCertificate, \
    GradeChoices, Publication
from abroadin.apps.data.applydata.utils import convert_pbt_overall_to_ibt_overall, \
    get_ielts_fake_sub_scores_based_on_overall, \
    get_toefl_fake_sub_scores_based_on_overall

APPLYPROFILE_CT = ContentType.objects.get(app_label='applyprofile', model='applyprofile')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ids', nargs='+', type=int)

    def handle(self, *args, **options):

        ids = options['ids']

        for obj in ApplyProfile.objects.exclude(id__in=ids):
            if Education.objects.filter(content_type=APPLYPROFILE_CT, object_id=obj.id).exists():
                Education.objects.filter(content_type=APPLYPROFILE_CT, object_id=obj.id).delete()
            if Publication.objects.filter(content_type=APPLYPROFILE_CT, object_id=obj.id).exists():
                Publication.objects.filter(content_type=APPLYPROFILE_CT, object_id=obj.id).delete()
            if LanguageCertificate.objects.filter(content_type=APPLYPROFILE_CT, object_id=obj.id).exists():
                LanguageCertificate.objects.filter(content_type=APPLYPROFILE_CT, object_id=obj.id).delete()
            obj.delete()
