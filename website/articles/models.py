from django import forms
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.functions import Coalesce

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from taggit.models import TaggedItemBase

from website.utils.blocks import StoryBlock
from website.utils.models import BasePage, RelatedPage


@register_snippet
class ArticlePageCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Article category"
        verbose_name_plural = "Article categories"


class ArticlePageRelatedPage(RelatedPage):
    source_page = ParentalKey(
        'articles.ArticlePage',
        related_name='related_pages'
    )


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ArticlePage(BasePage):
    template = 'patterns/pages/articles/articles_page.html'

    subpage_types = []
    parent_page_types = ['ArticleIndex']

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
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    categories = ParentalManyToManyField('articles.ArticlePageCategory', blank=True)

    # It's datetime for easy comparison with first_published_at
    publication_date = models.DateTimeField(
        null=True, blank=True,
        help_text="Use this field to override the date that the "
        "articles item appears to have been published."
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
        InlinePanel('authors', label="Authors"),
        SnippetChooserPanel('license'),
        FieldPanel('tags'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
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


class ArticlePageAuthor(Orderable):
    page = ParentalKey(
        ArticlePage,
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


class ArticleIndex(BasePage):
    template = 'patterns/pages/articles/articles_index.html'

    subpage_types = ['ArticlePage']
    parent_page_types = ['home.HomePage']

    introduction = models.TextField(blank=True)

    content_panels = BasePage.content_panels + [
        FieldPanel('introduction'),
    ]

    class Meta:
        verbose_name = "Articles Index"

    def get_context(self, request, *args, **kwargs):
        articles = ArticlePage.objects.live().public().descendant_of(self).annotate(
            date=Coalesce('publication_date', 'first_published_at')
        ).order_by('-date')
        extra_url_params = ''

        category = request.GET.get('category')
        if category:
            articles = articles.filter(categories__slug=category)
            extra_url_params = 'category=' + category

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(articles, settings.DEFAULT_PER_PAGE)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            articles=articles,
            # Only show articles types that have been used
            categories=ArticlePageCategory.objects.all().values_list('slug', 'name').distinct().order_by('name'),
            extra_url_params=extra_url_params,
        )
        return context
