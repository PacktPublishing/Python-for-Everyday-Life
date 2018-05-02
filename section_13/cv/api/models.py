# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


SCHOOL_KINDS = (
    ('Elementary school', 'Elementary school'),
    ('Middle school', 'Middle school'),
    ('High school', 'High school'),
    ('University/College', 'University/College'),
    ('Ph.D./Master', 'Ph.D./Master')
)

# --- API Resources Models ---

class Skill(models.Model):
    name = models.TextField(max_length=128, null=False, blank=False,
                            verbose_name="Skill",
                            help_text="Skill")
    level = models.IntegerField(null=False, blank=False,
                                validators=[
                                    MaxValueValidator(5),
                                    MinValueValidator(1)],
                                default=3,
                                verbose_name="Level of expertise",
                                help_text="Level of expertise")

    def __str__(self):
        return 'Skill: {} (pk={})'.format(self.name, self.pk if self.pk is not None else 'None')



class School(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False,
                            help_text="School name", verbose_name="School name")
    kind = models.CharField(max_length=64, choices=SCHOOL_KINDS, default='High school',
                            null=False, blank=False,
                            help_text="School kind", verbose_name="School kind")
    address = models.TextField(max_length=256, null=False, blank=False,
                               verbose_name="School address",
                               help_text="School address")
    start_date = models.DateField(null=False, blank=False,
                                  help_text="Start date",
                                  verbose_name="Start date")
    end_date = models.DateField(null=True, blank=True,
                                help_text="End date",
                                verbose_name="End date")
    final_mark = models.TextField(max_length=512, null=True, blank=True,
                                  verbose_name="School final assessment",
                                  help_text="School assessment")

    def save(self, *args, **kwargs):
        if self.end_date is not None:
            if self.start_date > self.end_date:
                raise IntegrityError('Start date must be before end date')
        super(School, self).save(*args, **kwargs)

    def __str__(self):
        return 'School: {} at {} (pk={})'.format(self.kind, self.name,
                                                 self.pk if self.pk is not None else 'None')

class WorkExperience(models.Model):
    company = models.TextField(max_length=128, null=False, blank=False,
                               verbose_name="Company name",
                               help_text="Company name")
    headline = models.TextField(max_length=128, null=True, blank=False,
                                verbose_name="Job headline",
                                help_text="Job headline")
    start_date = models.DateField(null=False, blank=False,
                                  help_text="Start date",
                                  verbose_name="Start date")
    end_date = models.DateField(null=True, blank=True,
                                help_text="End date",
                                verbose_name="End date")
    description = models.TextField(max_length=1024, null=False, blank=False,
                                   verbose_name="Job description",
                                   help_text="Job description")

    def save(self, *args, **kwargs):
        if self.end_date is not None:
            if self.start_date > self.end_date:
                raise IntegrityError('Start date must be before end date')
        super(WorkExperience, self).save(*args, **kwargs)

    def __str__(self):
        return 'Work experience: {} at {} (pk={})'.format(self.headline, self.company,
                                                 self.pk if self.pk is not None else 'None')


class Curriculum(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True,
                              related_name='cvs_set',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False, blank=False,
                            help_text="Name",
                            verbose_name="Name")
    surname = models.CharField(max_length=64, null=False, blank=False,
                               help_text="Surname",
                               verbose_name="Surname")
    birth_date = models.DateField(null=False, blank=False,
                                  help_text="Birth date",
                                  verbose_name="Birth date")
    birth_place = models.CharField(max_length=64, null=False, blank=False,
                                   help_text="Birth place",
                                   verbose_name="Birth place")
    address = models.TextField(max_length=256, null=False, blank=False,
                               verbose_name="Address",
                               help_text="Address")
    email = models.EmailField(null=False, blank=False,
                              help_text="Email address",
                              verbose_name="Email address")
    telephone = models.CharField(max_length=32, null=False, blank=False,
                                 help_text="Phone number",
                                 verbose_name="Phone number")
    website = models.URLField(null=True, blank=True,
                              help_text="Website URL",
                              verbose_name="Website URL")
    schools = models.ManyToManyField(School, blank=True,
                                     related_name="attended_schools",
                                     verbose_name="Attended schools")
    work_experiences = models.ManyToManyField(WorkExperience, blank=True,
                                              related_name="previous_work_experiences",
                                              verbose_name="Previous work experiences")
    skills = models.ManyToManyField(Skill, blank=True,
                                    related_name="skills_owned",
                                    verbose_name="Skills owned")

    def __str__(self):
        return 'CV of {} {} (pk={})'.format(self.name, self.surname,
                                            self.pk if self.pk is not None else 'None')

# --- Authentication Models ---

def one_year_away():
    return timezone.now() + timezone.timedelta(days=365)


class APIToken(models.Model):
    value = models.UUIDField(max_length=64, unique=True,
                             null=False, blank=False,
                             default=uuid.uuid4,
                             help_text="Token value",
                             verbose_name="Token value")
    owner = models.ForeignKey(User, null=False, blank=False,
                              related_name='users_set',
                              on_delete=models.CASCADE,
                              help_text="Owner",
                              verbose_name="Owner")
    expires_on = models.DateTimeField(null=False, blank=False,
                                      default=one_year_away,
                                      help_text="Expiration datetime",
                                      verbose_name="Expiration datetime")
    application = models.CharField(max_length=128, null=False, blank=False,
                                   help_text="App name",
                                   verbose_name="App name")

    def __str__(self):
        return 'Token ending with: {} owned by user: {}(pk={})'.format(
                    str(self.value)[-4:],
                    self.owner.pk,
                    self.pk if self.pk is not None else 'None')