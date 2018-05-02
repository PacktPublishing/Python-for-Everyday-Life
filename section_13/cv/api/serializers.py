# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from django.forms.models import model_to_dict

def curriculum_to_dict(cv):
    _dict = model_to_dict(cv)
    if cv.owner is not None:
        _dict['owner'] = cv.owner.pk
    _dict['schools'] = [model_to_dict(school) for school in cv.schools.all()]
    _dict['skills'] = [model_to_dict(skill) for skill in cv.skills.all()]
    _dict['work_experiences'] = [model_to_dict(wexp) for wexp in cv.work_experiences.all()]
    return _dict