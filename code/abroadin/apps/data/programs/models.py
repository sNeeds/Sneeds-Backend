from django.db import models

from abroadin.apps.data.applydata.models import Grade


class ProgramOtherFee(models.Model):
    name = models.CharField(max_length=1024)
    fee = models.FloatField(null=True, blank=True)


class Program(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    grade_text = models.CharField(max_length=1024, null=True, blank=True)

    min_length = models.IntegerField()
    max_length = models.IntegerField()
    coop_length = models.IntegerField(default=0)

    length_breakdown = models.CharField(max_length=1024, null=True, blank=True)
    tuition = models.IntegerField()
    application_fee = models.IntegerField()
    other_fees = models.ManyToManyField(ProgramOtherFee)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ProgramIntake(models.Model):
    class StatusChoices(models.TextChoices):
        OPEN = 'Open'
        CLOSED = 'Closed'

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    status = models.CharField(choices=StatusChoices.choices, max_length=256)
    start_date = models.DateField()
    open_date = models.DateField()
    deadline = models.DateField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ProgramOtherRequirement(models.Model):
    name = models.CharField(max_length=1024)


class ProgramRequirement(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    grade_text = models.CharField(max_length=1024, blank=True, null=True)
    min_gpa = models.FloatField()
    english_score_required = models.BooleanField()
    other_requirements = models.ManyToManyField(ProgramOtherRequirement)
    min_duolingo_score = models.FloatField()
    min_toefl_reading = models.FloatField()
    min_toefl_writing = models.FloatField()
    min_toefl_listening = models.FloatField()
    min_toefl_speaking = models.FloatField()
    min_toefl_total = models.FloatField()
    min_ielts_reading = models.FloatField()
    min_ielts_writing = models.FloatField()
    min_ielts_listening = models.FloatField()
    min_ielts_speaking = models.FloatField()
    min_ielts_average = models.FloatField()
