import csv
import json
import os
from argparse import ArgumentParser
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


def get_school_from_main_dict(loaded_dict):
    data = loaded_dict['data']['attributes']

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
        id=loaded_dict['data']['id'],
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
        living_cost=float(data['living_cost']) if data['living_cost'] is not None else None,
        avg_tuition=float(data['avg_tuition']) if data['avg_tuition'] is not None else None,
        total_students=data['total_students'],
        international_students=data['international_students'],
        coop_length=data['coop_length'],
        accommodation_types=data['accommodation_types'],
        conditional_acceptance=data['conditional_acceptance'],

        social=social,
        address=address,
        country_code=data['country_code']
    )

    return school


def edit_university(input_object: School, db_object: models.University):
    models.University.objects.filter(pk=db_object.pk).update(
        submission_through=input_object.submission_through,
        submission_path_note=input_object.submission_path_note,
        currency=input_object.currency,
        institution_type=input_object.institution_type,
        accommodation_types=input_object.accommodation_types,
        accommodation_information=input_object.accommodation_information,
        coop_participating=input_object.coop_participating,
        coop_length=input_object.coop_length,
        esl_is_academic_dependant=input_object.esl_is_academic_dependant,
        description=input_object.description,
        establishment_type=input_object.establishment_type,  # University, College or ...,
        founded_year=input_object.founded_year,
        living_cost=int(input_object.living_cost),
        avg_tuition=int(input_object.avg_tuition),
        total_students=input_object.total_students,
        international_students=input_object.international_students,
        conditional_acceptance=input_object.conditional_acceptance,
    )

    models.Address.objects.get_or_create(content_type__model='university', object_id=db_object.pk,
                                         defaults={
                                             'content_type': ContentType.objects.get_for_model(
                                                 models.University),
                                             'object_id': db_object.pk,
                                             'street': input_object.address.street,
                                             'city': input_object.address.city,
                                             'province': input_object.address.province,
                                             'postal': input_object.address.postal,
                                             'latitude': input_object.address.latitude,
                                             'longitude': input_object.address.longitude,
                                         })

    models.Social.objects.get_or_create(content_type__model='university', object_id=db_object.pk,
                                        defaults={
                                            'content_type': ContentType.objects.get_for_model(
                                                models.University),
                                            'object_id': db_object.pk,
                                            'video': input_object.social.video,
                                            'website': input_object.social.website,
                                            'facebook': input_object.social.facebook,
                                            'twitter': input_object.social.twitter,
                                            'linkedin': input_object.social.linkedin,
                                        })


def is_school_ok_to_add(school: School):
    if school.establishment_type in ['University'] and school.country == 'Canada':
        return True


def get_csv_row(match_status, input_case, db_case, fields, extra_detail='') -> list:
    row = [match_status]
    for field in fields:

        if input_case is not None:
            row.append(str(getattr(input_case, field)))
        else:
            row.append('NO_OBJECT')

        if db_case is not None:
            row.append(str(getattr(db_case, field)))
        else:
            row.append('NO_OBJECT')

    row.append(extra_detail)
    return row


class Command(BaseCommand):
    help = "For insert universities from folder contains json files."

    def add_arguments(self, parser: ArgumentParser):

        parser.add_argument('path', help='Absolute path of json containing dir.')
        parser.add_argument('--export_csv', action='store_true', help='Demonstrates export csv or not.')
        parser.add_argument('--csv_file_path', action='store', help='Absolute path of csv file.Note that he file'
                                                                    ' will be over writen if it exists.')
        parser.add_argument('--csv_fields', nargs='+')
        parser.add_argument('--export_text', action='store_true', help='Demonstrates export text or not.')
        parser.add_argument('--text_file_path', action='store', help='Absolute path of output text file.'
                                                                     'Note that the file will be '
                                                                     'over writen if it exists.')

    def handle(self, *args, **options):
        pprint(options)
        input_folder_path = options['path']
        export_csv = options['export_csv']
        csv_file_path = options['csv_file_path']
        csv_fields = options['csv_fields']
        export_text = options['export_text']
        text_file_path = options['text_file_path']

        if not input_folder_path or not os.path.isdir(input_folder_path):
            raise CommandError('The files containing directory is not valid.')

        if export_csv and not csv_file_path:
            raise CommandError('Export csv is enabled but csv path is not defined.')

        if export_csv:
            head, tail = os.path.split(csv_file_path)
            if not tail.endswith('.csv'):
                raise CommandError('No csv file is specified. Please specify a file in addition to dir.')
            if not os.path.isdir(head):
                raise CommandError('csv_file_path has not correct path end to the file.')

        if export_text and not text_file_path:
            raise CommandError('Export text is enabled but text path is not defined.')

        if export_text:
            head, tail = os.path.split(text_file_path)
            if not tail.endswith('.txt'):
                raise CommandError('No text file is specified. Please specify a file in addition to dir.')
            if not os.path.isdir(head):
                raise CommandError('text_file_path has not correct path end to the file.')

        if export_text:
            text_output_file = open(text_file_path, 'w+')
        if export_csv:
            csv_output_file = open(csv_file_path, 'w')
            csv_writer = csv.writer(csv_output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            first_row = ['match_status']
            for field in csv_fields:
                first_row.append(f'{field}(input)')
                first_row.append(f'{field}(db)')
            first_row.append('extra_details')
            csv_writer.writerow(first_row)

        all_files_num = 0
        processable_files_num = 0
        edited_count = 0
        existed_count = 0
        entries_count = 0
        added_countries = []
        success_schools = 0
        edit_unis = []
        dissimilars = []
        not_matched_count = 0
        doubt_objects = []
        failure_cases = []  # (type, description)

        for dirpath, dirs, files in os.walk(input_folder_path):
            for file_name in files:
                all_files_num += 1
                if all_files_num % 200 == 0:
                    self.stdout.write(
                        self.style.WARNING(' %s files are processed until now.' % str(all_files_num))
                    )
                if not file_name.endswith('json'):
                    continue

                with open(os.path.join(dirpath, file_name)) as f:
                    loaded_object = json.load(f)
                    if loaded_object.get('errors') or not loaded_object.get('data'):
                        failure_cases.append((None, None,
                                              f'Not University File: The file {file_name} does not'
                                              f' contain valuable data.'))
                        continue

                    school = get_school_from_main_dict(loaded_dict=loaded_object)

                    processable_files_num += 1

                    if not is_school_ok_to_add(school):
                        continue

                    entries_count += 1

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
                            edit_unis.append((school, db_university, f'similarity: {db_university.factor}'))

                            qs4 = qs3.filter(factor__lte=0.97)

                            if qs4.exists():
                                obj = qs4.first()
                                doubt_objects.append(('search::', school.id, school.name, obj.name, obj.search_rank,
                                                      ' factor: ', obj.factor))
                        else:
                            obj = qs.first()
                            not_matched_count += 1
                            if obj:
                                dissimilars.append((school, obj))
                            else:
                                dissimilars.append((school, None))

                    else:
                        obj = qs.first()
                        not_matched_count += 1
                        if obj:
                            dissimilars.append((school, obj))
                        else:
                            dissimilars.append((school, None))

        self.stdout.write(self.style.SUCCESS(
            'Start editing data base'
        ))

        processed_count = -1
        for case in edit_unis:
            if processed_count == -1:
                message = '\n\nMatched cases were:\n\n\n'
                if export_text:
                    text_output_file.write(message)
                else:
                    self.stdout.write(self.style.WARNING(message), ending='')
            # if processed_count == 0:
            #     break
            # print(edited_count)
            processed_count += 1
            if processed_count % 10 == 0:
                self.stdout.write(
                    self.style.WARNING(' %s universities are processed.' % str(processed_count))
                )
            try:
                with transaction.atomic():
                    edit_university(input_object=case[0], db_object=case[1])
                    edited_count += 1
                    message = f'Matched and edited successfully.\n' \
                              f'applyboard id:     {case[0].id}\n' \
                              f'abroadin id:       {case[1].id}\n' \
                              f'applyboard name:   {case[0].name}\n' \
                              f'abroadin name:     {case[1].name}\n' \
                              '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                    if export_text:
                        text_output_file.write(message)
                    else:
                        print(message)
                    if export_csv:
                        csv_writer.writerow(get_csv_row('MATCHED', case[0], case[1], csv_fields, case[2]))

            except IntegrityError as e:
                failure_cases.append((school, db_university, 'Error in DB editing\n' + str(e)))

        self.stdout.write(self.style.SUCCESS(
            'Editing data base finished'
        ))

        if export_text:
            text_output_file.write(
                '------------------------------------------------------------\n'
                '------------------------------------------------------------\n'
                '------------------------------------------------------------\n'
                '------------------------------------------------------------\n')
        else:
            print('------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n')

        message = '\n\nNot matched cases were:\n\n\n'
        if export_text:
            text_output_file.write(message)
        else:
            self.stdout.write(self.style.WARNING(message), ending='')

        for case in dissimilars:
            if case[1]:
                message = f'Potential similar case presents.\n' \
                          f'applyboard id:      {case[0].id}\n' \
                          f'abroadin id:        {case[1].id}\n' \
                          f'applyboard name:    {case[0].name}\n' \
                          f'abroadin name:      {case[1].name}\n' \
                          f'country:            {case[0].country}\n'
            else:
                message = f'Potential similar case Not Found!' \
                          f'applyboard id:     {case[0].id}\n' \
                          f'applyboard name:   {case[0].name}\n' \
                          f'country:           {case[0].country}\n'
            message += '-----------------------------------------------------------------------------------------\n'

            if export_text:
                text_output_file.write(message)
            else:
                print(message, end='')
            if export_csv:
                csv_writer.writerow(get_csv_row('JUST_SIMILAR', case[0], case[1], csv_fields, ))

        if export_text:
            text_output_file.write(
                '------------------------------------------------------------\n'
                '------------------------------------------------------------\n'
                '------------------------------------------------------------\n'
                '------------------------------------------------------------\n')
        else:
            print('------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n'
                  '------------------------------------------------------------\n')

        message = '\n\nFailure cases were:\n\n\n'
        if export_text:
            text_output_file.write(message)
        else:
            self.stdout.write(self.style.NOTICE(message), ending='')

        for case in failure_cases:
            message = f''
            if case[0] is not None:
                message += f'applyboard id:     {case[0].id}\n' \
                           f'applyboard name:   {case[0].name}\n'

            if case[1] is not None:
                message += f'abroadin id:       {case[1].id}\n' \
                           f'abroadin name:     {case[1].name}\n'

            message += f'Error detail:      {case[2]}\n'
            if case[0] is not None or case[1] is not None:
                message += '----------------------------------------------------------'

            if export_text:
                text_output_file.write(message)
            else:
                self.stdout.write(self.style.NOTICE(message), ending='')

            if export_csv:
                csv_writer.writerow(get_csv_row('FAILURE', case[0], case[1], csv_fields, case[2]))
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
        message = '\n"%s" files checked out and "%s" school detected. "%s" school were ok to add to db,' \
                  ' based on terms considered in "is_school_ok_to_add" function.\n' \
                  '"%s" university matched and edited successfully and ' \
                  '"%s" universities was not existed in db or not similar enough to edit.' \
                  ' so they need to insert or edit manually.\n FOR ASSURANCE CHECK MATCHED SECTION TOO!.\n' \
                  '"%s objects faced failure. Check failure section!!!' \
                  'Also "%s" countries added:' % (str(all_files_num),
                                                  str(processable_files_num),
                                                  str(entries_count),
                                                  str(edited_count),
                                                  str(not_matched_count),
                                                  str(len(failure_cases)),
                                                  str(len(added_countries)),
                                                  )

        if export_text:
            text_output_file.close()
            with open(text_file_path, 'r+') as text_output_file2:
                content = text_output_file2.read()
                text_output_file2.seek(0, 0)
                text_output_file2.write(message + '\n\n' + content)
            # content = text_output_file.read()
            # f.seek(0)
            # text_output_file.write(message + '\n\n' + content)
            # text_output_file2.close()

        self.stdout.write(self.style.SUCCESS(message))

        if export_csv:
            csv_output_file.close()
