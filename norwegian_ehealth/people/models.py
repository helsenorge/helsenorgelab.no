from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, StreamFieldPanel)
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from norwegian_ehealth.utils.blocks import StoryBlock
from norwegian_ehealth.utils.models import BasePage


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
    parent_page_types = ['home.HomePage']

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


"""
class PersonIndexPage(BasePage):
    template = 'patterns/pages/people/person_index_page.html'

    subpage_types = ['PersonPage']
    parent_page_types = ['home.HomePage']

    @cached_property
    def people(self):
        return self.get_children().specific().live().public()

    def get_context(self, request, *args, **kwargs):
        page_number = request.GET.get('page')
        paginator = Paginator(self.people, settings.DEFAULT_PER_PAGE)
        try:
            people = paginator.page(page_number)
        except PageNotAnInteger:
            people = paginator.page(1)
        except EmptyPage:
            people = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(people=people)

        return context
"""
