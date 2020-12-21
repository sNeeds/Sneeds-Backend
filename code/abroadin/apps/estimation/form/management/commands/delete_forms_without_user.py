from django.core.management import BaseCommand, CommandParser

from abroadin.apps.estimation.form.models import StudentDetailedInfo


class Command(BaseCommand):
    help = "By this command forms (StudentDetailedInfo objects), that haven't been assigned any user to them," \
           " will be deleted"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-l', '--liveperiod',
                            type=int,
                            help="Indicates how many past days should be ignored.Default is 3.")

    def handle(self, *args, **options):
        StudentDetailedInfo.objects.delete_forms_without_user(options.get('liveperiod'))
