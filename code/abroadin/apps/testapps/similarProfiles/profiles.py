from abroadin.apps.data.account.serializers import UniversitySerializer


class Profile(object):
    def __init__(self):
        self.match_percent = None
        self.language_certificate = None

        self.home_university = None
        self.home_major = None

        self.accepted_universities_number = None
        self.destination_university = None
        self.destination_major = None
        self.destination_grade = None
        self.destination_scholarship = None

        self.rejected_universities_number = None
        self.destination_rejected_university = None
        self.destination_rejected_year = None
        self.destination_rejected_major = None
        self.destination_rejected_scholarship = None

    def get_json(self):
        data = {
            "match_percent": self.match_percent,
            "language_certificate": self.language_certificate,
            "home": {
                "university": self.home_university.name,
                "country": self.home_university.country.name,
                "major": self.home_major.name
            },
            "accepted_destination": {
                "university": self.destination_university.name,
                "major": self.destination_major.name,
                "grade": self.destination_grade,
                "scholarship": self.destination_scholarship
            },
            "rejected_destination": {
                "university": self.destination_rejected_university.name,
                "year": self.destination_rejected_year,
                "major": self.destination_rejected_major.name,
                "scholarship": self.destination_rejected_scholarship
            },
            "accepted_universities_number": self.accepted_universities_number,
            "rejected_universities_number": self.rejected_universities_number,
        }

        return data



#
#
#     data = [
#         {
#             "home_university": self.get_home_university(form),
#             "home_university_gpa": self.get_home_university_gpa(form),
#             "applied_university": self.get_applied_university_data(form),
#             "major": self.get_major(form),
#             "grade": form.get_last_university_grade(),
#             "gpa": self.get_gpa(form),
#             "graduate_year": 2019,
#             "language_certificate": "IELTS 7.5 & GRE",
#             "fund": "30,000$/year",
#             "accepted": True
#         }
#     ]
#
#     class SimilarUniversitiesListView(CAPIView):
#         def get_form_obj(self, form_id):
#             try:
#                 return StudentDetailedInfo.objects.get(id=form_id)
#             except StudentDetailedInfo.DoesNotExist:
#                 return Http404
#
#         def get_home_university(self, form):
#             last_university_through = form.last_university_through()
#             return last_university_through.university.name if last_university_through is not None else None
#
#         def get_home_university_gpa(self, form):
#             last_university_through = form.last_university_through()
#             return last_university_through.gpa if last_university_through is not None else None
#
#         def get_major(self, form):
#             last_university_through = form.last_university_through()
#             return last_university_through.major.name if last_university_through is not None else None
#
#         def get_gpa(self, form):
#             last_university_through = form.last_university_through()
#             gpa = last_university_through.gpa if last_university_through is not None else None
#
#             if gpa:
#                 margin = (form.id.int % 30 - 15) / 10
#                 margin = min(margin, 1)
#                 margin = max(margin, -1)
#                 gpa += decimal.Decimal(margin)
#                 gpa = min(gpa, 20)
#                 gpa = max(0, gpa)
#
#             return gpa
#
#         def get_applied_university_data(self, form):
#             def _acceptable_university(universities, admission_chance):
#                 ACCEPTED_ADMISSION_CHANCE_VALUE = 0.5
#
#                 for university in universities:
#                     admission_chance_value = admission_chance.get_university_chance(university)["admission"]
#                     if ACCEPTED_ADMISSION_CHANCE_VALUE < admission_chance_value:
#                         return university
#
#                 return None
#
#             def _preferred_country_or_none(countries):
#                 canada = Country.objects.get(name="Canada")
#                 usa = Country.objects.get(name="United States")
#
#                 if canada in countries:
#                     return canada
#                 elif usa in countries:
#                     return usa
#
#                 return None
#
#             picked_universities = {
#                 "usa": [
#                     University.objects.get(name="Princeton University"),  # 12
#                     University.objects.get(name="University of Washington"),  # 73
#                     University.objects.get(name="University of Virginia"),  # 219
#                     University.objects.get(name="Colorado State University"),  # 443
#                 ],
#                 "canada": [
#                     University.objects.get(name="McGill University"),  # 33
#                     University.objects.get(name="University of Alberta"),  # 120
#                     University.objects.get(name="Université Laval"),  # 420
#                 ],
#                 "europe": [
#                     University.objects.get(name="École Polytechnique Fédérale de Lausanne (EPFL)"),  # 14,
#                     University.objects.get(name="The University of Melbourne"),  # 41,
#                     University.objects.get(name="Politecnico di Milano"),  # 137,
#                     University.objects.get(name="University of Trento"),  # 406,
#                 ]
#             }
#
#             admission_chance = AdmissionChance(form)
#             want_to_apply = form.get_want_to_apply_or_none()
#
#             if not want_to_apply:
#                 university = _acceptable_university(picked_universities["canada"], admission_chance)
#                 if university is None:
#                     university = picked_universities["canada"][-1]
#
#             elif not want_to_apply.universities.all().exists():
#                 countries = want_to_apply.countries.all()
#                 preferred_country = _preferred_country_or_none(countries)
#
#                 if preferred_country == Country.objects.get(name="United States"):
#                     universities = picked_universities["usa"]
#                 elif preferred_country == Country.objects.get(name="Canada"):
#                     universities = picked_universities["canada"]
#                 else:
#                     universities = picked_universities["europe"]
#
#                 university = _acceptable_university(universities, admission_chance)
#
#             else:
#                 universities = want_to_apply.universities.all().order_by('-rank')
#                 university = _acceptable_university(universities, admission_chance)
#                 if university is None:
#                     university = _acceptable_university(picked_universities["canada"], admission_chance)
#                     if university is None:
#                         university = picked_universities["canada"][-1]
#
#             return UniversitySerializer(university, context={"request": self.request}).data
#
#         def get(self, request, form_id, format=None):
#             form = self.get_form_obj(form_id)
#
#             data = [
#                 {
#                     "home_university": self.get_home_university(form),
#                     "home_university_gpa": self.get_home_university_gpa(form),
#                     "applied_university": self.get_applied_university_data(form),
#                     "major": self.get_major(form),
#                     "grade": form.get_last_university_grade(),
#                     "gpa": self.get_gpa(form),
#                     "graduate_year": 2019,
#                     "language_certificate": "IELTS 7.5 & GRE",
#                     "fund": "30,000$/year",
#                     "accepted": True
#                 }
#             ]
#
#         return Response(data)
