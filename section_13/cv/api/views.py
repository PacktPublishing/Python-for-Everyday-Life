# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import json
from datetime import datetime as dt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.views import View
from .models import Curriculum, Skill, School, WorkExperience, APIToken
from api.auth import with_valid_token, with_json_only
from .serializers import curriculum_to_dict
from .forms import SkillForm, SchoolForm, WorkExperienceForm, CurriculumForm


# --- API ENDPOINTS VIEWS ---

@method_decorator(with_valid_token, name='dispatch')
class TokenListView(View):

    def get(self, request, *args, **kwargs):
        try:
            tokens = APIToken.objects.filter(owner=request.user)
            data = [model_to_dict(token) for token in tokens]
        except APIToken.DoesNotExist:
            data = []
        return JsonResponse(data, status=200, safe=False)


@method_decorator(with_valid_token, name='dispatch')
@method_decorator(with_json_only, name='dispatch')
class CurriculumListView(View):

    def get(self, request, *args, **kwargs):
        try:
            cvs = Curriculum.objects.filter(owner=request.user)
            data = [curriculum_to_dict(cv) for cv in cvs]
        except Curriculum.DoesNotExist:
            data = []
        return JsonResponse(data, status=200, safe=False)

    def post(self, request, *args, **kwargs):
        # retrieve POST data
        data = json.loads(request.body.decode('utf-8'))

        # retrieve related REST resources
        try:
            schools = data['schools']
            wexps = data['work_experiences']
            skills = data['skills']
        except KeyError:
            return HttpResponseBadRequest()

        # now prepare params for creating a new protected CV with no related resources
        new_data = dict(data, schools=[], work_experiences=[], skills=[],
                        owner=request.user.pk)

        try:
            # step 1: create a new Curriculum instance with no related resources
            cv_form = CurriculumForm(new_data)  # create a model form
            new_cv = cv_form.save()  # validate and persist data.

            # step 2: now create all related REST resources (schools, work
            # experiences and skills)
            new_schools = [SchoolForm(school).save() for school in schools]
            new_wexps = [WorkExperienceForm(wexp).save() for wexp in wexps]
            new_skills = [SkillForm(skill).save() for skill in skills]

            # step 3: bind all related resources to the new CV
            new_cv.schools.add(*new_schools)
            new_cv.work_experiences.add(*new_wexps)
            new_cv.skills.add(*new_skills)

        except ValueError as e:
            print(e)
            return HttpResponseBadRequest()

        return JsonResponse(curriculum_to_dict(new_cv), status=201)


@method_decorator(with_json_only, name='dispatch')
class PublicCurriculumListView(View):

    def get(self, request, *args, **kwargs):
        try:
            public_cvs = Curriculum.objects.filter(owner__isnull=True)
            data = [curriculum_to_dict(cv) for cv in public_cvs]
        except Curriculum.DoesNotExist:
            data = []
        return JsonResponse(data, status=200, safe=False)

    def post(self, request, *args, **kwargs):
        # retrieve POST data
        data = json.loads(request.body.decode('utf-8'))

        # retrieve related REST resources
        schools = data['schools']
        wexps = data['work_experiences']
        skills = data['skills']

        # now prepare params for creating a new public CV with no related resources
        new_data = dict(data, schools=[], work_experiences=[], skills=[], owner=None)

        try:
            # step 1: create a new Curriculum instance with no related resources
            cv_form = CurriculumForm(new_data)  # create a model form
            new_cv = cv_form.save()  # validate and persist data.

            # step 2: now create all related REST resources (schools, work
            # experiences and skills)
            new_schools = [SchoolForm(school).save() for school in schools]
            new_wexps = [WorkExperienceForm(wexp).save() for wexp in wexps]
            new_skills = [SkillForm(skill).save() for skill in skills]

            # step 3: bind all related resources to the new CV
            new_cv.schools.add(*new_schools)
            new_cv.work_experiences.add(*new_wexps)
            new_cv.skills.add(*new_skills)

        except ValueError as e:
            print(e)
            return HttpResponseBadRequest()

        return JsonResponse(curriculum_to_dict(new_cv), status=201)


@method_decorator(with_valid_token, name='dispatch')
class CurriculumView(View):

    def get(self, request, cv_id, *args, **kwargs):
        try:
            cv = Curriculum.objects.get(id=cv_id, owner=request.user)
            data = curriculum_to_dict(cv)
            return JsonResponse(data, status=200, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()

    def delete(self, request, cv_id, *args, **kwargs):
        # this deletes also all related wexps, schools and skills!
        try:
            cv = Curriculum.objects.get(id=cv_id, owner=request.user)
            cv.work_experiences.all().delete()
            cv.schools.all().delete()
            cv.skills.all().delete()
            cv.delete()
            return JsonResponse('', status=204, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()


@method_decorator(with_valid_token, name='dispatch')
@method_decorator(with_json_only, name='dispatch')
class WorkExperienceListView(View):

    def get(self, request, cv_id, *args, **kwargs):
        # fetch query params
        str_date_from = request.GET.get('from', None)
        str_date_to = request.GET.get('to', None)

        # fetch all work experiences related to this CV
        try:
            wexps = Curriculum.objects.get(id=cv_id, owner=request.user).\
                work_experiences.all()
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()

        # case: no time boundaries specified
        if str_date_from is None and str_date_to is None:
            data = [model_to_dict(wexp) for wexp in wexps.all()]
        # case: time boundaries correctly specified
        elif str_date_from is not None and str_date_to is not None:
            try:
                date_from = dt.strptime(str_date_from, '%Y-%m-%d')
                date_to = dt.strptime(str_date_to, '%Y-%m-%d')
            except:
                return HttpResponseBadRequest()
            data = [model_to_dict(wexp) for wexp in wexps.filter(
                start_date__gte=date_from, start_date__lte=date_to)]
        else:
            return HttpResponseBadRequest()
        return JsonResponse(data, status=200, safe=False)

    def post(self, request, cv_id, *args, **kwargs):
        # retrieve POST data
        data = json.loads(request.body.decode('utf-8'))

        try:
            # step 1: retrieve the parent CV
            cv = Curriculum.objects.get(id=cv_id, owner=request.user)

            # step 2: create a new WorkExperience instance
            wexp_form = WorkExperienceForm(data)  # create a model form
            new_wexp = wexp_form.save()  # validate and persist data

            # step 3: bind the new WorkExperience to the parent CV
            cv.work_experiences.add(new_wexp)

        except ValueError:
            return HttpResponseBadRequest()
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()

        return JsonResponse(model_to_dict(new_wexp), status=201)


@method_decorator(with_valid_token, name='dispatch')
class LatestWorkExperienceView(View):

    def get(self, request, cv_id, *args, **kwargs):
        try:
            wexps = Curriculum.objects.get(id=cv_id, owner=request.user).\
                work_experiences.filter(end_date__isnull=True).order_by('-start_date')
            if wexps:
                data = model_to_dict(wexps[0])
            else:
                data = {}
            return JsonResponse(data, status=200, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()


@method_decorator(with_valid_token, name='dispatch')
class WorkExperienceView(View):

    def get(self, request, cv_id, workexp_id,  *args, **kwargs):
        try:
            wexp = Curriculum.objects.get(id=cv_id, owner=request.user).\
                work_experiences.get(id=workexp_id)
            data = model_to_dict(wexp)
            return JsonResponse(data, status=200, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()
        except WorkExperience.DoesNotExist:
            return HttpResponseNotFound()

    def delete(self, request, cv_id, workexp_id, *args, **kwargs):
        try:
            Curriculum.objects.get(id=cv_id, owner=request.user).\
                work_experiences.get(id=workexp_id).delete()
            return JsonResponse('', status=204, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()
        except WorkExperience.DoesNotExist:
            return HttpResponseNotFound()


@method_decorator(with_valid_token, name='dispatch')
@method_decorator(with_json_only, name='dispatch')
class SchoolListView(View):

    def get(self, request, cv_id, *args, **kwargs):
        # fetch query params
        str_date_from = request.GET.get('from', None)
        str_date_to = request.GET.get('to', None)

        # fetch all schools related to this CV
        try:
            schools = Curriculum.objects.get(id=cv_id, owner=request.user).\
                schools.all()
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()

        # case: no time boundaries specified
        if str_date_from is None and str_date_to is None:
            data = [model_to_dict(school) for school in schools.all()]
        # case: time boundaries correctly specified
        elif str_date_from is not None and str_date_to is not None:
            try:
                date_from = dt.strptime(str_date_from, '%Y-%m-%d')
                date_to = dt.strptime(str_date_to, '%Y-%m-%d')
            except:
                return HttpResponseBadRequest()
            data = [model_to_dict(school) for school in schools.filter(
                start_date__gte=date_from, start_date__lte=date_to)]
        else:
            return HttpResponseBadRequest()
        return JsonResponse(data, status=200, safe=False)

    def post(self, request, cv_id, *args, **kwargs):
        # retrieve POST data
        data = json.loads(request.body.decode('utf-8'))

        try:
            # step 1: retrieve the parent CV
            cv = Curriculum.objects.get(id=cv_id, owner=request.user)

            # step 2: create a new School instance
            school_form = SchoolForm(data)  # create a model form
            new_school = school_form.save()  # validate and persist data

            # step 3: bind the new School to the parent CV
            cv.schools.add(new_school)

        except ValueError:
            return HttpResponseBadRequest()
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()

        return JsonResponse(model_to_dict(new_school), status=201)


@method_decorator(with_valid_token, name='dispatch')
class SchoolView(View):

    def get(self, request, cv_id, school_id, *args, **kwargs):
        try:
            school = Curriculum.objects.get(id=cv_id, owner=request.user).\
                        schools.get(id=school_id)
            data = model_to_dict(school)
            return JsonResponse(data, status=200, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()
        except School.DoesNotExist:
            return HttpResponseNotFound()

    def delete(self, request, cv_id, school_id, *args, **kwargs):
        try:
            Curriculum.objects.get(id=cv_id, owner=request.user).\
                schools.get(id=school_id).delete()
            return JsonResponse('', status=204, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()
        except School.DoesNotExist:
            return HttpResponseNotFound()


@method_decorator(with_valid_token, name='dispatch')
@method_decorator(with_json_only, name='dispatch')
class SkillListView(View):

    def get(self, request, cv_id, *args, **kwargs):
        # fetch query params
        str_min_level = request.GET.get('min_level', None)

        # fetch all skills related to this CV
        try:
            skills = Curriculum.objects.get(id=cv_id, owner=request.user).\
                skills.all()
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()

        # case: no min_level specified
        if str_min_level is None :
            data = [model_to_dict(skill) for skill in skills.all()]
        # case: min_level correctly specified
        elif str_min_level is not None:
            try:
                min_level = int(str_min_level)
            except:
                return HttpResponseBadRequest()
            data = [model_to_dict(skill) for skill in skills.filter(level__gte=min_level)]
        else:
            return HttpResponseBadRequest()
        return JsonResponse(data, status=200, safe=False)


    def post(self, request, cv_id, *args, **kwargs):
        # retrieve POST data
        data = json.loads(request.body.decode('utf-8'))

        try:
            # step 1: retrieve the parent CV
            cv = Curriculum.objects.get(id=cv_id, owner=request.user)

            # step 2: create a new Skill instance
            skill_form = SkillForm(data)  # create a model form
            new_skill = skill_form.save()  # validate and persist data

            # step 3: bind the new Skill to the parent CV
            cv.skills.add(new_skill)

        except ValueError:
            return HttpResponseBadRequest()
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()

        return JsonResponse(model_to_dict(new_skill), status=201)


@method_decorator(with_valid_token, name='dispatch')
class SkillView(View):

    def get(self, request, cv_id, skill_id, *args, **kwargs):
        try:
            skill = Curriculum.objects.get(id=cv_id, owner=request.user).\
                        skills.get(id=skill_id)
            data = model_to_dict(skill)
            return JsonResponse(data, status=200, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()
        except Skill.DoesNotExist:
            return HttpResponseNotFound()

    def delete(self, request, cv_id, skill_id, *args, **kwargs):
        try:
            Curriculum.objects.get(id=cv_id, owner=request.user).\
                skills.get(id=skill_id).delete()
            return JsonResponse('', status=204, safe=False)
        except Curriculum.DoesNotExist:
            return HttpResponseNotFound()
        except Skill.DoesNotExist:
            return HttpResponseNotFound()