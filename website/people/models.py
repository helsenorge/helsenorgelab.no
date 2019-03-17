from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, StreamFieldPanel)
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from website.utils.blocks import StoryBlock
from website.utils.models import BasePage


class SocialMediaProfile(models.Model):
    person_page = ParentalKey(
        'PersonPage',
        related_name='social_media_profile'
    )
    site_titles = (
        ('twitter', "Twitter"),
        ('linkedin', "LinkedIn")
    )
    site_urls = (
        ('twitter', 'https://twitter.com/'),
        ('linkedin', 'https://www.linkedin.com/in/')
    )
    service = models.CharField(
        max_length=200,
        choices=site_titles
    )
    username = models.CharField(max_length=255)

    @property
    def profile_url(self):
        return dict(self.site_urls)[self.service] + self.username

    def clean(self):
        if self.service == 'twitter' and self.username.startswith('@'):
            self.username = self.username[1:]


class PersonPage(BasePage):
    template = 'patterns/pages/people/person_page.html'

    subpage_types = []
    parent_page_types = ['people.PersonIndexPage']

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    job_title = models.CharField(max_length=255)
    introduction = models.TextField(blank=True)
    biography = StreamField(StoryBlock(), blank=True)
    email = models.EmailField(blank=True)

    content_panels = BasePage.content_panels + [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
        ], heading="Name"),
        ImageChooserPanel('photo'),
        FieldPanel('job_title'),
        InlinePanel('social_media_profile', label='Social accounts'),
        MultiFieldPanel([
            FieldPanel('email'),
        ], heading='Contact information'),
        FieldPanel('introduction'),
        StreamFieldPanel('biography')
    ]


class PersonIndexPage(BasePage):
    template = 'patterns/pages/people/person_index_page.html'

    subpage_types = ['PersonPage']
    parent_page_types = ['home.HomePage']

    introduction = models.TextField(blank=True)

    content_panels = BasePage.content_panels + [
        FieldPanel('introduction'),
    ]

    class Meta:
        verbose_name = "People Index"

    def get_context(self, request, *args, **kwargs):
        people = PersonPage.objects.live().public().descendant_of(self).order_by('slug')

        page_number = request.GET.get('page', 1)
        paginator = Paginator(people, settings.DEFAULT_PER_PAGE)
        try:
            people = paginator.page(page_number)
        except PageNotAnInteger:
            people = paginator.page(1)
        except EmptyPage:
            people = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(people=people)

        return context
