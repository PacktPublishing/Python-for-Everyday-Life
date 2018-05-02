# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from django import forms
from .models import Curriculum, Skill, School, WorkExperience


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'


class SchoolForm(forms.ModelForm):
    # we override auto-generated form fields so what we can validate date format
    start_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                                 input_formats=(['%Y-%m-%d']))
    end_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                               input_formats=['%Y-%m-%d'],
                               required=False)

    class Meta:
        model = School
        fields = ['name', 'kind', 'address', 'start_date',
                  'end_date', 'final_mark']


class WorkExperienceForm(forms.ModelForm):
    # we override auto-generated form fields so what we can validate date format
    start_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                                 input_formats=(['%Y-%m-%d']))
    end_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                               input_formats=['%Y-%m-%d'],
                               required=False)

    class Meta:
        model = WorkExperience
        fields = ['company', 'headline', 'start_date', 'end_date', 'description']


class CurriculumForm(forms.ModelForm):
    # we override auto-generated form fields so what we can validate date format
    birth_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                                 input_formats=(['%Y-%m-%d']))

    class Meta:
        model = Curriculum
        fields = ['owner', 'name', 'surname', 'birth_date', 'birth_place',
                  'address', 'email', 'telephone', 'website', 'schools',
                  'work_experiences', 'skills']