from django.db import models

from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                         PageChooserPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from norwegian_ehealth.utils.models import BasePage


class HomePage(BasePage):
    template = 'patterns/pages/home/home_page.html'

    # Only allow creating HomePages at the root level
    parent_page_types = ['wagtailcore.Page']

    introduction = models.CharField(blank=True, max_length=255)

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
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )

    featured_page_1 = models.ForeignKey(
        'standardpages.InformationPage',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )

    featured_page_2 = models.ForeignKey(
        'standardpages.InformationPage',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )

    featured_page_3 = models.ForeignKey(
        'standardpages.InformationPage',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )

    featured_page_4 = models.ForeignKey(
        'standardpages.InformationPage',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )

    featured_page_5 = models.ForeignKey(
        'standardpages.InformationPage',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )

    featured_page_6 = models.ForeignKey(
        'standardpages.InformationPage',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
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
        MultiFieldPanel(
            [
                PageChooserPanel('featured_page_1'),
                PageChooserPanel('featured_page_2'),
                PageChooserPanel('featured_page_3'),
                PageChooserPanel('featured_page_4'),
                PageChooserPanel('featured_page_5'),
                PageChooserPanel('featured_page_6'),
            ], heading="Featured Articles",
        )
    ]
