from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from website.articles.models import ArticlePage
from website.news.models import NewsPage
from website.utils.models import BasePage


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
    subpage_types = ['news.NewsIndex', 'standardpages.InformationPage', 'articles.ArticleIndex',
                     'people.PersonIndexPage']

    hero_title = models.CharField(null=True, blank=False, max_length=80)

    hero_introduction = models.CharField(blank=False, max_length=255)

    hero_button_text = models.CharField(blank=True, max_length=55)

    hero_button_link = models.ForeignKey(
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
        index.SearchField('hero_introduction'),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('hero_title'),
                FieldPanel('hero_introduction'),
                FieldPanel('hero_button_text'),
                PageChooserPanel('hero_button_link'),
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

        if ArticlePage.objects.live().public().count() >= 1:
            latest_articles = ArticlePage.objects.live().public().order_by('-first_published_at')
            context['article_top'] = latest_articles[0]
            context['articles_row_1'] = latest_articles[1:4]
            context['articles_row_2'] = latest_articles[4:7]

            context['featured_row_1'] = self.featured_pages.all()[:3]
            context['featured_row_2'] = self.featured_pages.all()[3:6]

        if NewsPage.objects.live().public().count() >= 1:
            latest_news = NewsPage.objects.live().public().order_by('-first_published_at')
            context['latest_news_1'] = latest_news[0:4]
            context['latest_news_2'] = latest_news[4:8]
            context['latest_news_3'] = latest_news[8:12]

        return context
