import csv
import os
from pprint import pprint

from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity, SearchVector, SearchQuery, SearchRank
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Value

from sNeeds.apps.data.account.models import University, Country


class Command(BaseCommand):
    help = "For insert universities from csv file. QS Ranking universities should be at top of file."

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_path', nargs='+', type=str)

    def handle(self, *args, **options):
        added_count = 0
        existed_count = 0
        entries_count = 0
        added_countries = []

        csv_path = os.path.join(settings.BASE_DIR,
                                "apps/data/account/management/commands/universities/qs_universities.csv"
                                )
        with open(csv_path) as f:
            reader = csv.reader(f, delimiter=',')
            t = 0
            unsim = []
            unsim_ranks = []
            unsim_names = []
            doubt_objects = []
            vector = SearchVector('name', weight='A')

            for row in reader:
                entries_count += 1

                if entries_count % 250 == 0:
                    self.stdout.write(
                        self.style.WARNING(' %s universities are processed until now.' % str(entries_count))
                    )
                name = row[0]
                country, created = Country.objects.get_or_create(name=row[1],
                                                                 defaults={'search_name': row[1],
                                                                           'slug': row[1].lower().replace(' ', '_')})

                if created:
                    added_countries.append(row[1])

                if row[2] == 'Un':
                    row[2] = 13000
                rank = int(row[2])

                qs = University.objects.filter(country=country).annotate(similarity=TrigramSimilarity('name', name)). \
                    filter(similarity__gte=0.3).order_by('-similarity')
                # .filter(country=country)
                # .order_by('-similarity')

                # print(rank)
                if qs.exists():
                    t += 1
                    # obj = qs.first()
                    # print(name, '  -  ', obj.name, obj.similarity)
                    #     for obj in qs:
                    #         print(name, '  -  ', obj.name, obj.similarity)
                else:
                    unsim.append((rank, name))

                qs2 = qs.filter(similarity__lte=0.80).order_by('-similarity')
                if qs2.exists():
                    obj = qs2.first()
                    doubt_objects.append((name, obj.name, obj.similarity))
                    query = SearchQuery(name)
                    queryset = qs2.annotate(
                        rankk=SearchRank(
                            vector,
                            query,
                            normalization=Value(0),
                        )
                    ).filter(rankk__gte=0.05).order_by('-rankk')
                    if queryset.exists():
                        obj = queryset.first()
                        doubt_objects.append(('search:::::', name, obj.name, obj.similarity))

                # university, created = University.objects.get_or_create(
                #     name=name,
                #     defaults={'search_name': name,
                #               'rank': rank,
                #               'country': country,
                #               }
                # )
                # if created:
                #     added_count += 1
                # else:
                #     existed_count += 1
            print("similars are :", t)
            print('unsimilars are:')
            pprint(unsim)
            print('------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n')
            print('doubts are:')
            # pprint(doubt_objects)
            for doubt in doubt_objects:
                print(doubt)
        self.stdout.write(self.style.SUCCESS('"%s" universities imported from file. "%s" university added and '
                                             '"%s" universities was existed or were repeated.\n'
                                             'Also "%s" countries added:' % (str(entries_count),
                                                                             str(added_count),
                                                                             str(existed_count),
                                                                             str(len(added_countries))
                                                                             )
                                             )
                          )
