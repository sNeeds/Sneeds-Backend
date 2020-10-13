import csv

from django.core.management.base import BaseCommand, CommandError

from sNeeds.apps.data.account.models import Country


class Command(BaseCommand):
    help = "For insert Countries from csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', nargs='+', type=str)

    def handle(self, *args, **options):
        added_count = 0
        existed_count = 0
        entries_count = 0
        added_countries = []
        with open(options['csv_path'][0]) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                entries_count += 1
                name = row[0]
                country, created = Country.objects.get_or_create(
                    name=name, defaults={'search_name': name,
                                         'slug': name.lower().replace(' ', '_')})
                if created:
                    added_count += 1
                    added_countries.append(name)
                else:
                    existed_count += 1

        self.stdout.write(self.style.SUCCESS('"%s" countries imported from file. "%s" country added and "%s" country'
                                             ' was existed.\nAdded countries are "%s"' % (str(entries_count),
                                                                                          str(added_count),
                                                                                          str(existed_count),
                                                                                          str(added_countries),
                                                                                          )
                                             )
                          )
