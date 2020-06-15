import datetime

from django import forms
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                         StreamFieldPanel)
from wagtail.api import APIField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from grapple.models import GraphQLImage, GraphQLString
from taggit.models import TaggedItemBase

from website.utils.blocks import StoryBlock
from website.utils.models import BasePage


@register_snippet
class EventPageCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event category"
        verbose_name_plural = "Event categories"


class EventPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'EventPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class EventPage(BasePage):
    template = 'patterns/pages/events/event_page.html'

    subpage_types = []
    parent_page_types = ['EventIndex']

    summary = models.TextField(
        max_length=280,
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
    body = StreamField(StoryBlock())

    # Event time
    start_date = models.DateField()
    start_time = models.TimeField(
        blank=True,
        null=True
    )
    end_date = models.DateField(
        blank=True,
        null=True
    )
    end_time = models.TimeField(
        blank=True,
        null=True
    )

    # URLs for more information
    information_url = models.URLField("Mer informasjon", blank=True)
    tickets_url = models.URLField("Påmelding", blank=True)
    program_url = models.URLField("Program", blank=True)
    streaming_url = models.URLField("Direktestrømming", blank=True)

    # Location
    location_name = models.CharField(
        "Sted",
        max_length=250,
        blank=True,
    )

    # Address
    street_address = models.CharField(
        "Gateadresse",
        max_length=512,
        blank=True
    )
    postal_code = models.CharField(
        "Postnummer",
        max_length=12,
        blank=True
    )
    city = models.CharField(
        "Poststed",
        max_length=255,
        blank=True
    )
    country = models.CharField(
        "Land",
        max_length=128,
        blank=True
    )

    # Tags and categories
    tags = ClusterTaggableManager(through=EventPageTag, blank=True)
    categories = ParentalManyToManyField('events.EventPageCategory', blank=True)

    # Publication date for publishing events at a later time
    publication_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Use this field to set custom publish time for event."
    )

    search_fields = BasePage.search_fields + [
        index.SearchField('summary'),
        index.SearchField('body'),
        index.SearchField('city'),
        index.SearchField('location_name'),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel('summary'),
        MultiFieldPanel(
            [
                ImageChooserPanel('featured_image'),
                FieldPanel('featured_image_caption'),
            ],
            heading="Featured Image",
        ),
        StreamFieldPanel('body'),
        MultiFieldPanel(
            [
                FieldPanel('start_date'),
                FieldPanel('start_time'),
                FieldPanel('end_date'),
                FieldPanel('end_time')
            ],
            heading="Tidspunkt",
        ),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
        MultiFieldPanel(
            [
                FieldPanel('information_url'),
                FieldPanel('tickets_url'),
                FieldPanel('program_url'),
                FieldPanel('streaming_url')
            ],
            heading="Mer informasjon",
        ),
        MultiFieldPanel(
            [
                FieldPanel('location_name'),
                FieldPanel('street_address'),
                FieldPanel('postal_code'),
                FieldPanel('city'),
                FieldPanel('country'),
            ],
            heading="Sted for arrangentet",
        ),
    ]

    promote_panels = [
        FieldPanel('publication_date'),
    ] + BasePage.promote_panels

    # Export fields over REST API
    api_fields = [
        APIField('summary'),
        APIField('body'),
        APIField('featured_image', serializer=ImageRenditionField('fill-1920x1080')),
        APIField('featured_image_caption'),
        APIField('event_starts'),
        APIField('event_ends'),
    ]

    graphql_fields = [
        GraphQLString("summary"),
        GraphQLString("body"),
        GraphQLImage("featured_image", serializer=ImageRenditionField('fill-1920x1080')),
        GraphQLString("featured_image_caption"),
        GraphQLString('event_starts'),
        GraphQLString('event_ends'),
    ]

    class Meta:
        verbose_name = "Events"

    @property
    def event_starts(self):
        if self.start_time:
            return datetime.combine(self.start_date, self.start_time)
        else:
            return self.start_date

    @property
    def event_ends(self):
        if self.end_date:
            if self.end_time:
                return datetime.combine(self.end_date, self.end_time)
            else:
                return self.end_date
        else:
            return self.start_date

    @property
    def location(self):
        infos = []
        location_info = (self.location_name, self.street_address, self.postal_code + ' ' + self.city, self.country)
        for info in location_info:
            if info.strip():
                infos.append(info)
        return (', ').join(infos)


class EventIndex(BasePage):
    template = 'patterns/pages/events/event_index_page.html'

    subpage_types = ['EventPage']
    parent_page_types = ['home.HomePage']

    introduction = models.TextField(blank=True)
    body = RichTextField(blank=True, features=['bold', 'italic', 'link'])

    content_panels = BasePage.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('body', classname="full"),
    ]

    class Meta:
        verbose_name = "Events Index"

    def get_context(self, request, *args, **kwargs):
        events = EventPage.objects.live().public().descendant_of(self).order_by('start_date')
        extra_url_params = ''
        show_past = False

        # Need help with this - should filter past events or
        # upcoming events based on the past parameter from querystring
        # Ideally the upcoming events should include ongoing events:
        # (start_date < now < end_date)
        now = timezone.localtime()
        if request.GET.get('past'):
            events = events.filter(start_date__lt=now)
            show_past = True
        else:
            events = events.filter(start_date__gt=now + timezone.timedelta(-1))

        category = request.GET.get('category')
        if category:
            events = events.filter(categories__slug=category)
            extra_url_params = 'category=' + category

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(events, settings.DEFAULT_PER_PAGE)
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            events=events,
            show_past=show_past,
            # Only show events types that have been used
            categories=EventPageCategory.objects.all().values_list('slug', 'name').distinct().order_by('name'),
            extra_url_params=extra_url_params,
        )
        return context
