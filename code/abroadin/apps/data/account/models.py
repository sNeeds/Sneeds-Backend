from django.db import models
from django.contrib.auth import get_user_model

from .managers import CountryQuerySetManager, UniversityManager, MajorManager
from abroadin.apps.data.applydata import values

User = get_user_model()


def get_image_upload_path(sub_dir):
    return "account/images/" + sub_dir


def get_student_resume_path(instance, filename):
    return "account/files/form/{}/resume/{}".format(instance.id, filename)


class BasicFormField(models.Model):

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(max_length=256, unique=True)
    picture = models.ImageField(null=True, blank=True, upload_to=get_image_upload_path("country-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    objects = CountryQuerySetManager.as_manager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(blank=False, max_length=1024, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to=get_image_upload_path("university-pictures"))
    rank = models.PositiveIntegerField()
    is_college = models.BooleanField(default=False)

    objects = UniversityManager.as_manager()

    class Meta:
        ordering = ["name"]

    @property
    def value(self):
        rank = self.rank
        value = None
        if rank < values.GREAT_UNIVERSITY_RANK:
            value = 1
        elif values.GREAT_UNIVERSITY_RANK <= rank < values.GOOD_UNIVERSITY_RANK:
            value = 0.96
        elif values.GOOD_UNIVERSITY_RANK <= rank < values.AVERAGE_UNIVERSITY_RANK:
            value = 0.91
        elif values.AVERAGE_UNIVERSITY_RANK <= rank < values.BAD_UNIVERSITY_RANK:
            value = 0.75
        elif values.BAD_UNIVERSITY_RANK <= rank:
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
