from django.db import models
from django.contrib.auth import get_user_model

from .managers import CountryManager

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
    picture = models.ImageField(upload_to=get_image_upload_path("country-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    objects = CountryManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(max_length=1024, unique=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to=get_image_upload_path("university-pictures"))
    rank = models.PositiveIntegerField(blank=True, null=True)
    is_college = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    @property
    def value(self):
        rank = min(self.rank, 2000)
        rank = 2000 - rank
        return rank / 2000

    def __str__(self):
        return self.name


class Major(models.Model):
    name = models.CharField(max_length=256, unique=True)
    search_name = models.CharField(max_length=1024, unique=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(
        blank=False,
        null=True,
        upload_to=get_image_upload_path("field-of-study-pictures")
    )
    parent_major = models.ForeignKey(
        'self',
        on_delete=models.PROTECT
    )

    def __str__(self):
        self.name = self.name
        return self.name
