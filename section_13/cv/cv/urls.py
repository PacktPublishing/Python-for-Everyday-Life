# -*- coding: utf-8 -*-
# !/usr/bin/env python3

"""cv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from api.views import CurriculumListView, PublicCurriculumListView, \
    CurriculumView, WorkExperienceListView, LatestWorkExperienceView, \
    WorkExperienceView, SchoolListView, SchoolView, SkillListView, SkillView, \
    TokenListView


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Public endpoints
    path('cvs/public',
         csrf_exempt(PublicCurriculumListView.as_view()),
         name='public_cvs'),

    # Protected endpoints
    path('tokens',
         csrf_exempt(TokenListView.as_view()),
         name='tokens'),
    path('cvs',
         csrf_exempt(CurriculumListView.as_view()),
         name='cvs'),
    path('cvs/<int:cv_id>',
         csrf_exempt(CurriculumView.as_view()),
         name='cv'),
    path('cvs/<int:cv_id>/work-experiences',
         csrf_exempt(WorkExperienceListView.as_view()),
         name='work_experiences'),
    path('cvs/<int:cv_id>/work-experiences/latest',
         csrf_exempt(LatestWorkExperienceView.as_view()),
         name='latest_work_experience'),
    path('cvs/<int:cv_id>/work-experiences/<int:workexp_id>',
         csrf_exempt(WorkExperienceView.as_view()),
         name='work_experience'),
    path('cvs/<int:cv_id>/schools',
         csrf_exempt(SchoolListView.as_view()),
         name='schools'),
    path('cvs/<int:cv_id>/schools/<int:school_id>',
         csrf_exempt(SchoolView.as_view()),
         name='school'),
    path('cvs/<int:cv_id>/skills',
         csrf_exempt(SkillListView.as_view()),
         name='skills'),
    path('cvs/<int:cv_id>/skills/<int:skill_id>',
         csrf_exempt(SkillView.as_view()),
         name='skill')
]
