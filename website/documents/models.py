from django.db import models

from wagtail.documents.models import AbstractDocument
from wagtail.documents.models import Document as WagtailDocument

from grapple.models import GraphQLString


class CustomDocument(AbstractDocument):
    description = models.TextField(
        max_length=255,
        blank=True,
        null=True
    )
    admin_form_fields = WagtailDocument.admin_form_fields + (
        'description',
    )

    graphql_fields = (
        GraphQLString("description"),
    )
