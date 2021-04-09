import csv
import json
import os
from pprint import pprint
import random

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import TrigramSimilarity, SearchVector, SearchQuery, SearchRank
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Value, F
from django.db.utils import IntegrityError

import pycountry

from abroadin.apps.data.globaldata import models


def print_statistics(schools):
    data = {}
    for school in schools:
        key = f'{school.address.country}, {school.establishment_type} '
        type_number = data.get(key) or 0
        data[key] = type_number + 1

    for type, number in data.items():
        print(f'{type} number: {number}')


def print_obj_attrs(obj):
    for attr in dir(obj):
        val = getattr(obj, attr)
        print(f'{attr}: {val}')


def print_objs_attrs(objs, attrs):
    for obj in objs:
        for attr in attrs:
            print(f'{getattr(obj, attr)}', end='')
        print('')


def export_to_csv(file_name, schools):
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for school in schools:
            write_data = [school.id, school.name, school.slug, school.establishment_type, school.address.country]
            writer.writerow(write_data)


def filter_all_canada_universities(schools):
    ret_schools = []
    for school in schools:
        if school.address.country == 'Canada' and school.establishment_type == 'University':
            ret_schools.append(school)

    return ret_schools


all_schools = []


class Social:
    def __init__(self, video, website, facebook, twitter, linkedin):
        self.video = video
        self.website = website
        self.facebook = facebook
        self.twitter = twitter
        self.linkedin = linkedin


class Address:
    def __init__(self, street, city, province, postal, country, latitude, longitude):
        self.street = street
        self.city = city
        self.province = province
        self.postal = postal
        self.country = country
        self.latitude = latitude
        self.longitude = longitude


class School:
    def __init__(
            self, id, name, slug, submission_through, submission_path_note,
            currency, institution_type, accommodation_information, coop_participating,
            esl_is_academic_dependant, description, establishment_type, founded_year, living_cost, avg_tuition,
            total_students, international_students, coop_length,
            accommodation_types, conditional_acceptance,
            social, address,
            country_code
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.submission_through = submission_through
        self.submission_path_note = submission_path_note
        self.currency = currency
        self.institution_type = institution_type
        self.accommodation_types = accommodation_types
        self.accommodation_information = accommodation_information
        self.coop_participating = coop_participating
        self.coop_length = coop_length
        self.esl_is_academic_dependant = esl_is_academic_dependant
        self.description = description
        self.establishment_type = establishment_type  # University, College or ...
        self.founded_year = founded_year
        self.living_cost = living_cost
        self.avg_tuition = avg_tuition
        self.total_students = total_students
        self.international_students = international_students
        self.conditional_acceptance = conditional_acceptance

        self.social = social
        self.address = address
        self.country = pycountry.countries.get(alpha_2=country_code).name

    def __str__(self):
        return self.name


def is_school_ok_to_add(school: School):
    if school.establishment_type in ['University'] and school.country == 'Canada':
        return True


class Command(BaseCommand):
    help = "For insert universities from csv file. QS Ranking universities should be at top of file."

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='?', default='')

    def handle(self, *args, **options):
        edited_count = 0
        existed_count = 0
        entries_count = 0
        added_countries = []
        success_schools = 0
        edit_unis = []
        unsim = []
        not_mathced_count = 0
        unsim_names = []
        doubt_objects = []
        failure_cases = []
        input_folder_path = options['path']
        if not input_folder_path:
            input_folder_path = settings.BASE_DIR + '/' + 'apps/data/globaldata/management/commands/schools'

        for i in range(3):
            entries_count += 1

            if entries_count % 200 == 0:
                self.stdout.write(
                    self.style.WARNING(' %s schools are processed until now.' % str(entries_count))
                )
            with open(input_folder_path + f'/{i}.json') as f:
                loaded_object = json.load(f)
                if loaded_object.get('errors'):
                    continue

                data = loaded_object['data']['attributes']

                address = Address(
                    street=data['address']['street'],
                    city=data['address']['city'],
                    province=data['address']['province'],
                    postal=data['address']['postal'],
                    country=data['address']['country'],
                    latitude=data['geo_location']['latitude'],
                    longitude=data['geo_location']['longitude'],
                )

                social = Social(
                    video=data['social_urls']['video'],
                    website=data['social_urls']['website'],
                    facebook=data['social_urls']['facebook'],
                    twitter=data['social_urls']['twitter'],
                    linkedin=data['social_urls']['linkedin'],
                )

                school = School(
                    id=i,
                    name=data['name'],
                    slug=data['slug'],
                    submission_through=data['submission_through'],
                    submission_path_note=data['submission_path_note'],
                    currency=data['currency'],
                    institution_type=data['institution_type'],
                    accommodation_information=data['accommodation_information'],
                    coop_participating=data['coop_participating'],
                    esl_is_academic_dependant=data['esl_is_academic_dependant'],
                    description=data['description'],
                    establishment_type=data['establishment_type'],
                    founded_year=data['founded_year'],
                    living_cost=data['living_cost'],
                    avg_tuition=data['avg_tuition'],
                    total_students=data['total_students'],
                    international_students=data['international_students'],
                    coop_length=data['coop_length'],
                    accommodation_types=data['accommodation_types'],
                    conditional_acceptance=data['conditional_acceptance'],

                    social=social,
                    address=address,
                    country_code=data['country_code']
                )

                if is_school_ok_to_add(school):
                    vector = SearchVector('name', weight='A')
                    country = models.Country.objects.get(name=school.country)
                    qs = models.University.objects.filter(country=country).annotate(
                        similarity=TrigramSimilarity('name', school.name)). \
                        filter(similarity__gte=0.1).order_by('-similarity')

                    if qs.exists():
                        obj = qs.first()
                        # doubt_objects.append((name, obj.name, obj.similarity))
                        query = SearchQuery(school.name)

                        qs2 = qs.filter(pk=obj.pk).annotate(
                            search_rank=SearchRank(
                                vector,
                                query,
                                normalization=Value(0),
                            )
                        )
                        qs3 = qs2.annotate(factor=F('similarity') * F('search_rank')).filter(factor__gte=0.50).order_by(
                            '-factor')
                        if qs3.exists():
                            # print('similar found')
                            success_schools += 1
                            db_university = qs3.first()
                            edit_unis.append((school, db_university, address, social))

                            qs4 = qs3.filter(factor__lte=0.97)

                            if qs4.exists():
                                obj = qs4.first()
                                doubt_objects.append(('search::', school.id, school.name, obj.name, obj.search_rank,
                                                      ' factor: ', obj.factor))
                        else:
                            obj = qs.first()
                            not_mathced_count += 1
                            if obj:
                                unsim.append((school.id, obj.id, school.name, obj.name, country))
                            else:
                                unsim.append((school.id, school.name, country))

                    else:
                        obj = qs.first()
                        not_mathced_count += 1
                        if obj:
                            unsim.append((school.id, obj.id, school.name, obj.name, country))
                        else:
                            unsim.append((school.id, school.name, country))

        self.stdout.write(
            'similars are : %s .' % str(success_schools)
        )
        self.stdout.write(self.style.SUCCESS(
            'Start editing data base'
        ))

        # qs = University.objects.filter(rank__lte=1005)
        # for obj in qs:
        #     new_rank = random.randint(1000 + int(obj.rank / 5), 1200 + int(obj.rank / 5))
        #     University.objects.filter(pk=obj.pk).update(rank=new_rank)
        processed_count = -1
        for case in edit_unis:

            # print(edited_count)
            processed_count += 1
            if processed_count % 10 == 0:
                self.stdout.write(
                    self.style.WARNING(' %s universities are processed.' % str(processed_count))
                )
            try:
                with transaction.atomic():
                    models.University.objects.filter(pk=case[1].pk).update(
                        submission_through=case[0].submission_through,
                        submission_path_note=case[0].submission_path_note,
                        currency=case[0].currency,
                        institution_type=case[0].institution_type,
                        accommodation_types=case[0].accommodation_types,
                        accommodation_information=case[0].accommodation_information,
                        coop_participating=case[0].coop_participating,
                        coop_length=case[0].coop_length,
                        esl_is_academic_dependant=case[0].esl_is_academic_dependant,
                        description=case[0].description,
                        establishment_type=case[0].establishment_type,  # University, College or ...,
                        founded_year=case[0].founded_year,
                        living_cost=int(case[0].living_cost),
                        avg_tuition=case[0].avg_tuition,
                        total_students=case[0].total_students,
                        international_students=case[0].international_students,
                        conditional_acceptance=case[0].conditional_acceptance,
                    )

                    models.Address.objects.get_or_create(content_type__model='university', object_id=case[1].pk,
                                                         defaults={
                                                             'content_type': ContentType.objects.get_for_model(
                                                                 models.University),
                                                             'object_id': case[1].pk,
                                                             'street': case[0].address.street,
                                                             'city': case[0].address.city,
                                                             'province': case[0].address.province,
                                                             'postal': case[0].address.postal,
                                                             'latitude': case[0].address.latitude,
                                                             'longitude': case[0].address.longitude,
                                                         })

                    models.Social.objects.get_or_create(content_type__model='university', object_id=case[1].pk,
                                                        defaults={
                                                            'content_type': ContentType.objects.get_for_model(
                                                                models.University),
                                                            'object_id': case[1].pk,
                                                            'video': case[0].social.video,
                                                            'website': case[0].social.website,
                                                            'facebook': case[0].social.facebook,
                                                            'twitter': case[0].social.twitter,
                                                            'linkedin': case[0].social.linkedin,
                                                        })

                    edited_count += 1
                    print('Matched and edited successfully.')
                    print('applyboard id:     ', case[0].id)
                    print('abroadin id:       ', case[1].id)
                    print('applyboard name:   ', case[0].name)
                    print('abroadin name:     ', case[1].name)
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            except IntegrityError:
                failure_cases.append({'id': case[0],
                                      'similar_name': case[1],
                                      'qs_name': case[2],
                                      'country': case[5],
                                      'similar_rank': case[3],
                                      'qs_rank': case[4],
                                      })
        self.stdout.write(self.style.SUCCESS(
            'Editing data base finished'
        ))
        # pprint(edit_unis)
        print('------------------------------------------------------------\n'
              '------------------------------------------------------------\n'
              # '------------------------------------------------------------\n'
              # '------------------------------------------------------------\n'
              # '------------------------------------------------------------\n'
              '------------------------------------------------------------\n'
              '------------------------------------------------------------\n')
        self.stdout.write(self.style.WARNING('Not matched cases were:'))
        # pprint(unsim)
        for case in unsim:
            if len(case) > 3:
                print('Potential case presents.')
                print('applyboard id:     ', case[0])
                print('abroadin id:       ', case[1])
                print('applyboard name:   ', case[2])
                print('abroadin name:     ', case[3])
                print('country:           ', case[4])
            else:
                print('Potential case Not Found!')
                print('applyboard id:     ', case[0])
                print('applyboard name:   ', case[1])
                print('country:           ', case[2])
            print('-----------------------------------------------------------------------------------------')

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
                                                                             str(edited_count),
                                                                             str(not_mathced_count),
                                                                             str(len(failure_cases)),
                                                                             str(len(added_countries)),
                                                                             )
                                             )
                          )
