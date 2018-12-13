from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import StreamField, RichTextField


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(help_text="Leave blank to use the page's own title", required=False)

    class Meta:
        template = 'patterns/molecules/navigation/blocks/menu_item.html',


class LinkColumnWithHeader(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text="Leave blank if no header required.")
    links = blocks.ListBlock(LinkBlock())

    class Meta:
        template = 'patterns/molecules/navigation/blocks/footer_column.html',


@register_setting(icon='list-ul')
class NavigationSettings(BaseSetting, ClusterableModel):
    primary_navigation = StreamField(
        [('link', LinkBlock()), ],
        blank=True,
        help_text="Main site navigation"
    )
    footer_links = StreamField(
        [('link', LinkBlock()), ],
        blank=True,
        help_text="Single list of elements at the base of the page."
    )

    footer_bottom_text = RichTextField(
        blank=True,
        help_text="Small print text at the bottom of all pages. Not required."
    )

    panels = [
        StreamFieldPanel('primary_navigation'),
        StreamFieldPanel('footer_links'),
        FieldPanel('footer_bottom_text'),
    ]
