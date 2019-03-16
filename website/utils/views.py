from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.views import defaults


def favicon(request):
    try:
        favicon_path = settings.FAVICON_STATIC_PATH
    except AttributeError:
        raise Http404
    return redirect(static(favicon_path))


def robots(request):
    content = "\n".join([
        "User-Agent: *",
        "Disallow: /search/",
        "Allow: /",
    ])
    return HttpResponse(content, content_type='text/plain')


def page_not_found(request, exception, template_name='patterns/pages/wagtail/404.html'):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name='patterns/pages/wagtail/500.html'):
    return defaults.server_error(request, template_name)
