from django.contrib.syndication.views import Feed

from website.articles.models import ArticlePage
from website.news.models import NewsPage


class ArticlesFeed(Feed):
    title = "RSS for artikler"
    link = "/rss/articles"
    description = "Alle artikler som er publisert"

    def items(self):
        return ArticlePage.objects.live().order_by('-first_published_at')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.introduction


class NewsFeed(Feed):
    title = "RSS for nyheter"
    link = "/rss/news"
    description = "Alle nyheter som er publisert"

    def items(self):
        return NewsPage.objects.live().order_by('-first_published_at')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary
