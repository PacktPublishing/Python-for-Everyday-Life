# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from django.contrib import admin

from .models import Skill, WorkExperience, School, Curriculum, APIToken

class SkillAdmin(admin.ModelAdmin):
    pass

class WorkExperienceAdmin(admin.ModelAdmin):
    pass

class SchoolAdmin(admin.ModelAdmin):
    pass

class CurriculumAdmin(admin.ModelAdmin):
    pass

class APITokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(Skill, SkillAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(APIToken, APITokenAdmin)
