# -*- coding: utf-8 -*-
#
#    Django error tracker default value
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET
from error_tracker.django import get_exception_model

model = get_exception_model()


@require_GET
def view_list(request):
    """
    Home page that lists mose recent exceptions
    :param request: request object
    :return:  rendered template
    """
    title = "App Error"
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    error = False
    errors = model.get_exceptions_per_page(page_number=page)
    next_url = reverse('view_errors') + "?page=" + str(errors.next_num) \
        if errors.has_next else None
    prev_url = reverse('view_errors') + "?page=" + str(errors.prev_num) \
        if errors.has_prev else None

    return render(request, template_name='list.html',
                  context=dict(error=error, title=title, errors=errors,
                               next_url=next_url, prev_url=prev_url))


@require_GET
def delete_exception(request, rhash):
    """
    Delete an exceptions
    :param request:  request object
    :param rhash:  hash key of the exception
    :return: redirect back to home page
    """
    model.delete_entity(rhash)
    return redirect(reverse('view_errors'))


@require_GET
def detail(request, rhash):
    """
    Display a specific page of the exception
    :param request: request object
    :param rhash:  hash key of the exception
    :return: detailed view
    """
    obj = model.get_entity(rhash)
    error = False
    if obj is None:
        raise Http404
    title = "%s : %s" % (obj.method, obj.path)
    return render(request, template_name='detail.html',
                  context=dict(error=error, title=title, obj=obj))
