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
        'standardpages.StandardPage',
        related_name='+',
        on_delete=models.CASCADE,
        verbose_name='featured page',
    )
    title = models.CharField(null=True, blank=True, max_length=80)
    summary = models.TextField(null=True, blank=True, max_length=200)
    image = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    panels = [
        PageChooserPanel('featured_page'),
        FieldPanel('title'),
        FieldPanel('summary'),
        ImageChooserPanel('image')
    ]


class HomePage(BasePage):
    template = 'patterns/pages/home/home_page.html'

    # Only allow creating HomePages at the root level
    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['news.NewsIndex', 'standardpages.StandardPage', 'articles.ArticleIndex',
                     'people.PersonIndex', 'events.EventIndex']

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

    articles_title = models.CharField(null=True, blank=True, max_length=150)
    articles_link = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )
    articles_linktext = models.CharField(null=True, blank=True, max_length=80)

    featured_pages_title = models.CharField(null=True, blank=True, max_length=150)
    pages_link = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )
    pages_linktext = models.CharField(null=True, blank=True, max_length=80)

    news_title = models.CharField(null=True, blank=True, max_length=150)
    news_link = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )
    news_linktext = models.CharField(null=True, blank=True, max_length=80)

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
        MultiFieldPanel(
            [
                FieldPanel('articles_title'),
                PageChooserPanel('articles_link'),
                FieldPanel('featured_pages_title'),
                PageChooserPanel('pages_link'),
                FieldPanel('news_title'),
                PageChooserPanel('news_link'),
            ], heading="Front page sections",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['articles_title'] = self.articles_title
        context['articles_link'] = self.articles_link
        context['articles_linktext'] = self.articles_linktext
        context['featured_pages_title'] = self.featured_pages_title
        context['pages_link'] = self.pages_link
        context['pages_linktext'] = self.pages_linktext
        context['news_title'] = self.news_title
        context['news_link'] = self.news_link
        context['news_linktext'] = self.news_linktext

        if ArticlePage.objects.live().public().count() >= 1:
            latest_articles = ArticlePage.objects.live().public().order_by('-first_published_at')
            context['article_top'] = latest_articles[0]
            context['articles_row_1'] = latest_articles[1:4]
            context['articles_row_2'] = latest_articles[4:7]

            context['featured_row_1'] = self.featured_pages.all()[:3]
            context['featured_row_2'] = self.featured_pages.all()[3:6]

        if NewsPage.objects.live().public().count() >= 1:
            latest_news = NewsPage.objects.live().public().order_by('-first_published_at')
            context['latest_news'] = latest_news[0:8]

        return context
