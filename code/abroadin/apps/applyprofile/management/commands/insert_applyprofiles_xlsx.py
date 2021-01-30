from pprint import pprint
from openpyxl import load_workbook, Workbook
from django.core.management import BaseCommand

from ...models import ApplyProfile, Admission

from abroadin.apps.data.account.models import University, Country, Major
from abroadin.apps.data.applydata.models import Education, RegularLanguageCertificate, Grade


phd = Grade.objects.filter(name__iexact='ph.d').first()
bachelor = Grade.objects.filter(name__iexact='bachelor').first()
master = Grade.objects.filter(name__iexact='master').first()

default_enroll_year = 2018


def _get_suitable_grade(grade_text):

    if grade_text.lower() == 'doctorate':
        return phd
    elif grade_text.lower() == 'masters':
        return master
    elif grade_text.lower() == 'bachelors':
        return bachelor
    raise Exception("grade not in right format")


class Command(BaseCommand):
    # https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/
    # https://docs.python.org/3/library/argparse.html#action

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='?', default='')

    def handle(self, *args, **options):
        wb3 = Workbook()
        ws = wb3.create_sheet()
        # ws.
        wb = load_workbook(options['path'])
        # print(wb.sheetnames)
        # print(wb['Sheet3'].values)
        # print(wb['Sheet3'].dimensions)
        # print(wb['Sheet3'].rows)
        # print(wb['Sheet3'].cell(1, 1).value)
        # print(wb['Sheet3'].max_row)
        # print(wb['Sheet3'].max_column)

        faulty_rows = []

        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            for i in range(2, sheet.max_row):
                # l = []
                # for j in range(1, sheet.max_column):
                #     l.append(str(sheet.cell(i, j).value))
                proceed_possible = True
                if isinstance(sheet.cell(i, 1).value, int):
                    try:
                        major = Major.objects.get(pk=sheet.cell(i, 1).value)
                    except Major.DoesNotExist or ValueError or TypeError:
                        faulty_rows.append((i, 'major does not exist'))
                        proceed_possible = False
                else:
                    faulty_rows.append((i, 'major wrong format'))
                    proceed_possible = False

                if isinstance(sheet.cell(i, 2).value, int):
                    try:
                        destination = University.objects.get(pk=sheet.cell(i, 2).value)
                    except University.DoesNotExist or ValueError or TypeError:
                        faulty_rows.append((i, 'destination does not exist'))
                        proceed_possible = False
                else:
                    faulty_rows.append((i, 'destination wrong format'))
                    proceed_possible = False

                if isinstance(sheet.cell(i, 3).value, str):
                    try:
                        grade = _get_suitable_grade(sheet.cell(i, 3).value)
                    except Exception as e:
                        faulty_rows.append((i, str(e)))
                        proceed_possible = False
                else:
                    faulty_rows.append((i, 'grade wrong format'))
                    proceed_possible = False

                if isinstance(sheet.cell(i, 4).value, int):
                    scholarship = sheet.cell(i, 4).value
                elif sheet.cell(i, 4).value is None:
                    scholarship = 0
                else:
                    faulty_rows.append((i, 'fund wrong format'))

                if isinstance(sheet.cell(i, 5).value, float):
                    bachelor_gpa = sheet.cell(i, 5).value
                    if isinstance(sheet.cell(i, 6).value, int):
                        try:
                            bachelor_university = University.objects.get(pk=sheet.cell(i, 6).value)
                        except University.DoesNotExist or ValueError or TypeError:
                            faulty_rows.append((i, 'bachelor_university does not exist'))
                    elif isinstance(sheet.cell(i, 6).value, str):
                        # TODO Do something for #N/A universities
                        bachelor_university = None
                    else:
                        bachelor_university = None
                else:
                    bachelor_gpa = None

                if isinstance(sheet.cell(i, 7).value, float):
                    master_gpa = sheet.cell(i, 7).value
                    if isinstance(sheet.cell(i, 8).value, int):
                        try:
                            master_university = University.objects.get(pk=sheet.cell(i, 8).value)
                        except University.DoesNotExist or ValueError or TypeError:
                            faulty_rows.append((i, 'master_university does not exist'))
                    else:
                        master_university = None
                else:
                    master_gpa = None

                if isinstance(sheet.cell(i, 15).value, int):
                    enroll_year = sheet.cell(i, 4).value
                elif sheet.cell(i, 4).value is None or isinstance(sheet.cell(i, 15).value, str):
                    enroll_year = default_enroll_year
                else:
                    faulty_rows.append((i, 'enroll_year wrong format'))



                ######################################################

                if proceed_possible:
                    apply_profile = ApplyProfile.objects.create(
                        name='Student #{}'.format(i)
                    )



                    # print(i, str(major).strip(), destination)

                # print(', '.join(l))

        pprint(faulty_rows)
