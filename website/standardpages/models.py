from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from website.utils.blocks import StoryBlock
from website.utils.models import BasePage, RelatedPage


class StandardPageCategory(models.Model):
    page = ParentalKey(
        'standardpages.InformationPage',
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


class InformationPageRelatedPage(RelatedPage):
    source_page = ParentalKey('InformationPage', related_name='related_pages')


class InformationPage(BasePage):
    template = 'patterns/pages/standardpages/information_page.html'

    introduction = models.TextField(blank=True)
    body = StreamField(StoryBlock())
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
    biography = models.CharField(
        help_text="Use this field to override the author's biography "
        "on this page.",
        max_length=255,
        blank=True
    )

    search_fields = BasePage.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
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
    ]

    class Meta:
        verbose_name = "Standard Page"


class InformationPageAuthor(Orderable):
    page = ParentalKey(
        InformationPage,
        related_name='authors'
    )
    author = models.ForeignKey(
        'people.PersonPage',
        on_delete=models.CASCADE
    )
    biography = models.CharField(
        help_text="Use this field to override the author's biography "
        "on this information page.",
        max_length=255,
        blank=True
    )

    panels = [
        PageChooserPanel('author'),
        FieldPanel('biography'),
    ]

"""
class IndexPage(BasePage):
    template = 'patterns/pages/standardpages/index_page.html'

    introduction = models.TextField(blank=True)

    content_panels = BasePage.content_panels + [
        FieldPanel('introduction'),
    ]

    search_fields = BasePage.search_fields + [
        index.SearchField('introduction'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        subpages = self.get_children().live()
        per_page = settings.DEFAULT_PER_PAGE
        page_number = request.GET.get('page')
        paginator = Paginator(subpages, per_page)

        try:
            subpages = paginator.page(page_number)
        except PageNotAnInteger:
            subpages = paginator.page(1)
        except EmptyPage:
            subpages = paginator.page(paginator.num_pages)

        context['subpages'] = subpages

        return context
"""
