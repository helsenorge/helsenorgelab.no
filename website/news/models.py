from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.functions import Coalesce

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from website.utils.blocks import StoryBlock
from website.utils.models import BasePage, RelatedPage


class NewsPageCategory(models.Model):
    page = ParentalKey(
        'news.NewsPage',
        related_name='categories'
    )
    category = models.ForeignKey(
        'utils.Category',
        related_name='+',
        on_delete=models.CASCADE,
        verbose_name='category',
    )

    panels = [
        FieldPanel('category')
    ]

    def __str__(self):
        return self.category.title


class NewsPageRelatedPage(RelatedPage):
    source_page = ParentalKey(
        'news.NewsPage',
        related_name='related_pages'
    )


class NewsPage(BasePage):
    template = 'patterns/pages/news/news_page.html'

    subpage_types = []
    parent_page_types = ['NewsIndex']

    introduction = models.TextField(
        blank=True,
        max_length=165,
    )
    featured_image = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    image_caption = models.CharField(
        blank=True,
        max_length=250,
    )
    body = StreamField(StoryBlock())
    license = models.ForeignKey(
        'utils.LicenseSnippet',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # It's datetime for easy comparison with first_published_at
    publication_date = models.DateTimeField(
        null=True, blank=True,
        help_text="Use this field to override the date that the "
        "news item appears to have been published."
    )

    search_fields = BasePage.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body')
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel('introduction'),
        MultiFieldPanel(
            [
                ImageChooserPanel('featured_image'),
                FieldPanel('image_caption'),
            ],
            heading="Featured Image",
        ),
        StreamFieldPanel('body'),
        InlinePanel('categories', label="Categories"),
        InlinePanel('authors', label="Authors"),
        SnippetChooserPanel('license'),
        FieldPanel('publication_date'),
        # TODO: comment related_pages back in if we have time with the front-end work for articles
        # InlinePanel('related_pages', label="Related pages"),
    ]

    class Meta:
        verbose_name = "Article"

    @property
    def display_date(self):
        if self.publication_date:
            return self.publication_date
        else:
            return self.first_published_at


class NewsPageAuthor(Orderable):
    page = ParentalKey(
        NewsPage,
        related_name='authors'
    )
    author = models.ForeignKey(
        'people.PersonPage',
        on_delete=models.CASCADE
    )
    biography = models.CharField(
        help_text="Use this field to override the author's biography "
        "on this article page.",
        max_length=255,
        blank=True
    )

    panels = [
        PageChooserPanel('author'),
        FieldPanel('biography'),
    ]


class NewsIndex(BasePage):
    template = 'patterns/pages/news/news_index.html'

    subpage_types = ['NewsPage']
    parent_page_types = ['home.HomePage']

    introduction = models.TextField(blank=True)

    content_panels = BasePage.content_panels + [
        FieldPanel('introduction'),
    ]

    class Meta:
        verbose_name = "Articles Index"

    def get_context(self, request, *args, **kwargs):
        news = NewsPage.objects.live().public().descendant_of(self).annotate(
            date=Coalesce('publication_date', 'first_published_at')
        ).order_by('-date')
        extra_url_params = ''

        category = request.GET.get('category')
        if category:
            news = news.filter(categories__category=category)
            extra_url_params = 'category=' + category

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(news, settings.DEFAULT_PER_PAGE)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            news=news,
            # Only show news types that have been used
            categories=NewsPageCategory.objects.all().values_list(
                'category__pk', 'category__title'
            ).distinct().order_by('category__title'),
            extra_url_params=extra_url_params,
        )
        return context
