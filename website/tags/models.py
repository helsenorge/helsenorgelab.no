from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from website.news.models import NewsPage
from website.utils.models import BasePage


class BlogTagPage(BasePage):
    template = 'patterns/pages/tags/tag_page.html'

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        newspages = NewsPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['newspages'] = newspages
        return context
