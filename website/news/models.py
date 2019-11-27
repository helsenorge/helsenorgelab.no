from django import forms
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.functions import Coalesce

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from grapple.models import GraphQLImage, GraphQLString
from taggit.models import TaggedItemBase

from website.utils.models import BasePage, RelatedPage


@register_snippet
class NewsPageCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "News category"
        verbose_name_plural = "News categories"


class NewsPageRelatedPage(RelatedPage):
    source_page = ParentalKey(
        'news.NewsPage',
        related_name='related_pages'
    )


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'NewsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class NewsPage(BasePage):
    template = 'patterns/pages/news/news_page.html'

    subpage_types = []
    parent_page_types = ['NewsIndex']

    introduction = models.TextField(
        max_length=165,
    )
    featured_image = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    featured_image_caption = models.CharField(
        blank=True,
        max_length=250,
    )
    body = RichTextField(blank=True, features=['bold', 'italic', 'link'])
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    categories = ParentalManyToManyField('news.NewsPageCategory', blank=True)

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
        FieldPanel('body', classname="full"),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
        MultiFieldPanel(
            [
                ImageChooserPanel('featured_image'),
                FieldPanel('featured_image_caption'),
            ],
            heading="Featured Image",
        ),
        FieldPanel('publication_date'),
    ]

    class Meta:
        verbose_name = "News"

    @property
    def display_date(self):
        if self.publication_date:
            return self.publication_date
        else:
            return self.first_published_at


class NewsIndex(BasePage):
    template = 'patterns/pages/news/news_index.html'

    subpage_types = ['NewsPage']
    parent_page_types = ['home.HomePage']

    introduction = models.TextField(blank=True)

    content_panels = BasePage.content_panels + [
        FieldPanel('introduction'),
    ]

    class Meta:
        verbose_name = "News Index"

    def get_context(self, request, *args, **kwargs):
        news = NewsPage.objects.live().public().descendant_of(self).annotate(
            date=Coalesce('publication_date', 'first_published_at')
        ).order_by('-date')
        extra_url_params = ''

        category = request.GET.get('category')
        if category:
            news = news.filter(categories__slug=category)
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
            categories=NewsPageCategory.objects.all().values_list('slug', 'name').distinct().order_by('name'),
            extra_url_params=extra_url_params,
        )
        return context
