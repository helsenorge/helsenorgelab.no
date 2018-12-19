from wagtail.contrib.modeladmin.options import (ModelAdmin, ModelAdminGroup,
                                                modeladmin_register)

from norwegian_ehealth.news.models import NewsType
# from norwegian_ehealth.people.models import PersonType


class NewsTypeModelAdmin(ModelAdmin):
    model = NewsType
    menu_icon = 'tag'


"""
class PersonTypeModelAdmin(ModelAdmin):
    model = PersonType
    menu_icon = 'tag'
"""


class TaxonomiesModelAdminGroup(ModelAdminGroup):
    menu_label = "Taxonomies"
    items = (
        NewsTypeModelAdmin,
        # PersonTypeModelAdmin,
    )
    menu_icon = 'tag'


modeladmin_register(TaxonomiesModelAdminGroup)
