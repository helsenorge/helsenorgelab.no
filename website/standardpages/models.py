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


class StandardPageRelatedPage(RelatedPage):
    source_page = ParentalKey('StandardPage', related_name='related_pages')


class StandardPage(BasePage):
    template = 'patterns/pages/standardpages/information_page.html'

    subpage_types = ['standardpages.StandardPage']

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
        InlinePanel('authors', label="Authors"),
    ]

    class Meta:
        verbose_name = "Standard Page"


class StandardPageAuthor(Orderable):
    page = ParentalKey(
        StandardPage,
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
