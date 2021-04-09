from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model

from .managers import CountryManager, UniversityManager, MajorManager
from ..applydata.values.education import GREAT_UNIVERSITY_RANK, GOOD_UNIVERSITY_RANK, AVERAGE_UNIVERSITY_RANK, \
    BAD_UNIVERSITY_RANK

User = get_user_model()


def get_image_upload_path(sub_dir):
    return "globaldata/images/" + sub_dir


def get_student_resume_path(instance, filename):
    return "globaldata/files/form/{}/resume/{}".format(instance.id, filename)


class BasicFormField(models.Model):

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(max_length=256, unique=True)
    picture = models.FileField(
        null=True, blank=True, upload_to=get_image_upload_path("country-pictures"),
        validators=[FileExtensionValidator(['svg'])]
    )
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    objects = CountryManager.as_manager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class University(models.Model):
    class EstablishmentTypeChoices(models.TextChoices):
        COLLEGE = 'College'
        ENGLISH_INSTITUTE = 'English Institute'
        UNIVERSITY = 'University'
        HIGH_SCHOOL = 'High School'

    class AccommodationTypesChoices(models.TextChoices):
        OFF_CAMPUS_ON_CAMPUS = 'off-campus and on-campus'

    class InstitutionTypeChoices(models.TextChoices):
        PUBLIC = 'Public'
        PRIVATE = 'Private'

    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(blank=False, max_length=1024, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to=get_image_upload_path("university-pictures"))
    rank = models.PositiveIntegerField()
    is_college = models.BooleanField(default=False)

    submission_through = models.CharField(max_length=128, null=True, blank=True)
    submission_path_note = models.CharField(max_length=256, null=True, blank=True)
    currency = models.CharField(max_length=4, null=True, blank=True)
    institution_type = models.CharField(max_length=16, null=True, blank=True)
    accommodation_types = models.CharField(max_length=32, null=True, blank=True)
    accommodation_information = models.TextField(null=True, blank=True)
    coop_participating = models.BooleanField(null=True, blank=True)
    coop_length = models.IntegerField(null=True, blank=True)
    esl_is_academic_dependant = models.BooleanField(null=True, blank=True)
    establishment_type = models.CharField(max_length=32, null=True, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    living_cost = models.IntegerField(null=True, blank=True)
    avg_tuition = models.IntegerField(null=True, blank=True)
    total_students = models.IntegerField(null=True, blank=True)
    international_students = models.IntegerField(null=True, blank=True)
    conditional_acceptance = models.TextField(null=True, blank=True)

    objects = UniversityManager.as_manager()

    class Meta:
        ordering = ["name"]

    @property
    def value(self):
        rank = self.rank
        value = None
        if rank < GREAT_UNIVERSITY_RANK:
            value = 1
        elif GREAT_UNIVERSITY_RANK <= rank < GOOD_UNIVERSITY_RANK:
            value = 0.96
        elif GOOD_UNIVERSITY_RANK <= rank < AVERAGE_UNIVERSITY_RANK:
            value = 0.91
        elif AVERAGE_UNIVERSITY_RANK <= rank < BAD_UNIVERSITY_RANK:
            value = 0.75
        elif BAD_UNIVERSITY_RANK <= rank:
            value = 0.6

        return value

    def __str__(self):
        return self.name


class Major(models.Model):
    name = models.CharField(max_length=256)
    search_name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    objects = MajorManager.as_manager()

    def hierarchy_str(self):
        name = self.name
        if self.parent:
            name += " -> " + self.parent.hierarchy_str()
        return name

    def top_nth_parent(self, nth):
        parents_list = []
        parent = self.parent

        while parent:
            parents_list.insert(0, parent)
            parent = parent.parent

        try:
            return parents_list[nth - 1]
        except IndexError:
            return self

    def get_all_children_majors(self):
        qs = Major.objects.filter(parent=self)
        self_obj_qs = Major.objects.filter(id=self.id)
        if not qs.exists():
            return self_obj_qs
        return qs.get_all_children_majors() | self_obj_qs

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    province = models.CharField(max_length=32, null=True, blank=True)
    postal = models.CharField(max_length=16, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 'object_id',
    )


class Social(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 'object_id',
    )

    video = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
