from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from norwegian_ehealth.news.models import NewsPage
from norwegian_ehealth.utils.models import BasePage


class HomePageFeaturedPage(Orderable):
    page = ParentalKey(
        'home.HomePage',
        related_name='featured_pages'
    )
    featured_page = models.ForeignKey(
        'standardpages.InformationPage',
        related_name='+',
        on_delete=models.CASCADE,
        verbose_name='featured page',
    )

    panels = [
        PageChooserPanel('featured_page')
    ]


class HomePage(BasePage):
    template = 'patterns/pages/home/home_page.html'

    # Only allow creating HomePages at the root level
    parent_page_types = ['wagtailcore.Page']

    introduction = models.CharField(blank=False, max_length=255)

    button_text = models.CharField(blank=True, max_length=55)

    button_link = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )

    featured_image = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    search_fields = BasePage.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('introduction'),
                FieldPanel('button_text'),
                PageChooserPanel('button_link'),
                ImageChooserPanel('featured_image'),
            ], heading="Hero Section",
        ),
        InlinePanel(
            'featured_pages',
            label="Featured Pages",
            max_num=6,
            heading='Featured Pages, Maximum 6'
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        latest_articles = NewsPage.objects.live().public().order_by('-publication_date')
        article_top = latest_articles[0]
        articles_row_1 = latest_articles[1:4]
        articles_row_2 = latest_articles[4:7]
        context['article_top'] = article_top
        context['articles_row_1'] = articles_row_1
        context['articles_row_2'] = articles_row_2
        context['featured_row_1'] = self.featured_pages.all()[:3]
        context['featured_row_2'] = self.featured_pages.all()[3:6]

        return context
