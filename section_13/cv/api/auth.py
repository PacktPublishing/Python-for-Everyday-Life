# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import uuid
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from .models import APIToken

def with_valid_token(viewfunction):
    """
    Check that a valid API Token is provided with requests targeting this View
    :param viewfunction: the View to be decorated
    :return: function
    """
    def wrapped_viewfunction(request, *args, **kwargs):
        # check a token has been submitted and is a valid UUID
        # (Django lowercases header names and prefixes them with: HTTP_)
        token_value = request.META.get('HTTP_AUTHORIZATION', None)
        if not token_value:
            return HttpResponse(status=401)
        try:
            uuid.UUID(token_value)
        except ValueError:
            return HttpResponseBadRequest()

        try:
            # check the token is known
            token = APIToken.objects.get(value=token_value)
            # check the token has not expired
            assert timezone.now() <= token.expires_on
        except APIToken.DoesNotExist:
            return HttpResponse(status=401)
        except AssertionError:
            return HttpResponse(status=401)

        request.user = token.owner
        return viewfunction(request, *args, **kwargs)

    return wrapped_viewfunction

def with_json_only(viewfunction):
    """
    Check that on POSTs and PUTs the provided request body is JSON
    :param viewfunction: the View to be decorated
    :return: function
    """
    def wrapped_viewfunction(request, *args, **kwargs):
        if request.method in ['POST', 'PUT']:
            # check requests are marked with Content-Type: application/json
            if not request.content_type.startswith('application/json'):
                return HttpResponse(status=415)
        return viewfunction(request, *args, **kwargs)

    return wrapped_viewfunction