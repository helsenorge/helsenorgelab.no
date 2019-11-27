from django.apps import apps
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns

from grapple import urls as grapple_urls

from website.rss.feeds import ArticlesFeed, NewsFeed
from website.search import views as search_views
from website.utils.cache import get_default_cache_control_decorator
from website.utils.views import favicon, robots

from .api import api_router

# Private URLs are not meant to be cached.
private_urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    # Search cache-control headers are set on the view itself.
    path('search/', search_views.search, name='search'),
]


# Public URLs that are meant to be cached.
urlpatterns = [
    url(r'^api/v2/', api_router.urls),
    url(r"", include(grapple_urls)),
    url(r'rss/articles', ArticlesFeed()),
    url(r'rss/news', NewsFeed()),
    path('sitemap.xml', sitemap),
    path('favicon.ico', favicon),
    path('robots.txt', robots),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # Add views for testing 404 and 500 templates
        path('test404/', TemplateView.as_view(template_name='patterns/pages/wagtail/404.html')),
        path('test500/', TemplateView.as_view(template_name='patterns/pages/wagtail/500.html')),
    ]


# Style guide
if getattr(settings, 'PATTERN_LIBRARY_ENABLED', False) and apps.is_installed('pattern_library'):
    private_urlpatterns += [
        path('pattern-library/', include('pattern_library.urls')),
    ]


# Set public URLs to use the "default" cache settings.
urlpatterns = decorate_urlpatterns(urlpatterns,
                                   get_default_cache_control_decorator())

# Set vary header to instruct cache to serve different version on different
# cookies, different request method (e.g. AJAX) and different protocol
# (http vs https).
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    vary_on_headers('Cookie', 'X-Requested-With', 'X-Forwarded-Proto',
                    'Accept-Encoding')
)

# Join private and public URLs.
urlpatterns = private_urlpatterns + urlpatterns + [
    # Add Wagtail URLs at the end.
    # Wagtail cache-control is set on the page models's serve methods.
    path('', include(wagtail_urls)),
]

# Error handlers
handler404 = 'website.utils.views.page_not_found'
handler500 = 'website.utils.views.server_error'
