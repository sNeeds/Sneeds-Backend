import csv

from django.core.management.base import BaseCommand, CommandError

from sNeeds.apps.data.account.models import University, Country


class Command(BaseCommand):
    help = "For insert universities from csv file. QS Ranking universities should be at top of file."

    def add_arguments(self, parser):
        parser.add_argument('csv_path', nargs='+', type=str)

    def handle(self, *args, **options):
        added_count = 0
        existed_count = 0
        entries_count = 0
        added_countries = []
        with open(options['csv_path']) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                entries_count += 1
                name = row[0]
                country, created = Country.objects.get_or_create(name=row[1], defaults={'search_name': row[1]})

                if created:
                    added_countries.append(row[1])

                rank = int(row[2])
                if entries_count > 1010 and rank < 1000:
                    rank = 1050

                university, created = University.objects.get_or_create(name=name, defaults={'search_name': name,
                                                                                            'rank': rank,
                                                                                            'country': country})
                if created:
                    added_count += 1
                else:
                    existed_count += 1

        self.stdout.write(self.style.SUCCESS('"%s" universities imported from file. "%s" university added and '
                                             '"%s" universities was existed or were repeated.\n'
                                             'Also "%s" countries added.' % (str(entries_count),
                                                                             str(added_count),
                                                                             str(existed_count),
                                                                             str(len(added_countries))
                                                                             )
                                             )
                          )
