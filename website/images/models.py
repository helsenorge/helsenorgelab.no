from django.db import models

from wagtail.images.models import AbstractImage, AbstractRendition, Image


# We define our own custom image class to replace wagtailimages.Image,
# providing various additional data fields
class CustomImage(AbstractImage):
    license = models.ForeignKey(
        'utils.LicenseSnippet',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = models.TextField(
        blank=True,
        max_length=165,
    )
    author = models.CharField(
        blank=True,
        max_length=165,
        null=True,
    )
    image_source_url = models.URLField(
        blank=True
    )

    admin_form_fields = Image.admin_form_fields + (
        'description',
        'author',
        'license',
        'image_source_url'
    )


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        'CustomImage',
        related_name='renditions',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
