from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index

from norwegian_ehealth.utils.models import BasePage


class HomePage(BasePage):
    template = 'patterns/pages/home/home_page.html'

    # Only allow creating HomePages at the root level
    parent_page_types = ['wagtailcore.Page']

    strapline = models.CharField(blank=True, max_length=255)

    search_fields = BasePage.search_fields + [
        index.SearchField('strapline'),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel('strapline'),
    ]
