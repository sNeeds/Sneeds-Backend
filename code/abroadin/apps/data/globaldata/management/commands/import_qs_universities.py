import csv
import os
from pprint import pprint
import random

from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity, SearchVector, SearchQuery, SearchRank
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Value, F
from django.db.utils import IntegrityError

from abroadin.apps.data.globaldata.models import University, Country


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
                                "apps/data/globaldata/management/commands/universities/qs_universities.csv"
                                )
        with open(csv_path) as f:
            reader = csv.reader(f, delimiter=',')
            t = 0
            unsim = []
            unsim_count = 0
            unsim_names = []
            doubt_objects = []
            failure_cases = []

            edit_unis = []
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
                    filter(similarity__gte=0.59).order_by('-similarity')
                # .filter(country=country)
                # .order_by('-similarity')

                # print(rank)

                # if qs.exists():
                # t += 1
                # obj = qs.first()
                # print(name, '  -  ', obj.name, obj.similarity)
                #     for obj in qs:
                #         print(name, '  -  ', obj.name, obj.similarity)

                # qs2 = qs.filter(similarity__lte=0.9).order_by('-similarity')
                if qs.exists():
                    obj = qs.first()
                    # doubt_objects.append((name, obj.name, obj.similarity))
                    query = SearchQuery(name)
                    queryset = qs.filter(pk=obj.pk).annotate(
                        rankk=SearchRank(
                            vector,
                            query,
                            normalization=Value(0),
                        )
                    ).order_by('-rankk')
                    qs3 = queryset.annotate(factor=F('similarity') * F('rankk')).filter(factor__gte=0.50)
                    if qs3.exists():
                        t += 1
                        uni = qs3.first()
                        edit_unis.append((uni.pk, uni.name, name, uni.rank, rank, country))

                        qs4 = qs3.filter(factor__lte=0.97)

                        if qs4.exists():
                            obj = qs4.first()
                            doubt_objects.append(('search::', name, obj.name, obj.rankk,
                                                  ' factor: ', obj.factor))
                    else:
                        unsim_count += 1
                        unsim.append((name, country, rank))

                else:
                    unsim_count += 1
                    unsim.append((name, country, rank))

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
            self.stdout.write(
                'similars are : %s .' % str(t)
            )
            self.stdout.write(
                'start editing data base'
            )

            qs = University.objects.filter(rank__lte=1005)
            for obj in qs:
                new_rank = random.randint(1000 + int(obj.rank / 5), 1200 + int(obj.rank / 5))
                University.objects.filter(pk=obj.pk).update(rank=new_rank)
            for uni in edit_unis:
                
                # print(added_count)
                if added_count % 100 == 0:
                    self.stdout.write(
                        self.style.WARNING(' %s universities are edited in db.' % str(added_count))
                    )
                try:
                    University.objects.filter(pk=uni[0]).update(search_name=uni[2], name=uni[2], rank=uni[4])
                    added_count += 1
                except IntegrityError:
                    failure_cases.append({'id': uni[0],
                                          'similar_name': uni[1],
                                          'qs_name': uni[2],
                                          'country': uni[5],
                                          'similar_rank': uni[3],
                                          'qs_rank': uni[4],
                                          })
            self.stdout.write(
                'editing data base finished'
            )
            print('------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  # '------------------------------------------------------------\n'
                  # '------------------------------------------------------------\n'
                  # '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n')
            self.stdout.write(self.style.WARNING('Dissimilar cases were:'))
            pprint(unsim)

            print('------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  # '------------------------------------------------------------\n'
                  # '------------------------------------------------------------\n'
                  # '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n')

            self.stdout.write(self.style.NOTICE('Failure cases were:'))
            self.stdout.write(self.style.NOTICE(str(failure_cases)))
            # pprint(failure_cases)
            # print('doubts are:')
            # pprint(doubt_objects)
            # count = 0
            # doubt_objects.sort(key=lambda x: x[5])
            # for v in zip(doubt_objects):
            #     print(*v)
            # for doubt in doubt_objects:
            #     if doubt[0] != 'search::':
            #         print()
            #     print(doubt)
        self.stdout.write(self.style.SUCCESS('"%s" universities imported from file. "%s" university edited and "%s" '
                                             'universities was not existed in db so they need to insert or edit '
                                             'manually.\n'
                                             ' "%s objects failed to update and they need to insert manually.!!!'
                                             'Also "%s" countries added:' % (str(entries_count),
                                                                             str(added_count),
                                                                             str(unsim_count),
                                                                             str(len(failure_cases)),
                                                                             str(len(added_countries)),
                                                                             )
                                             )
                          )
