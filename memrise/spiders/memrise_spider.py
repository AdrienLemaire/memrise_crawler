from urlparse import urljoin
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from memrise.items import MemriseItem
from memrise.settings import USER, PASSWORD


class MemriseSpider(CrawlSpider):
    name = "memrise"
    allowed_domains = ["memrise.com"]
    start_urls = [
        "http://www.memrise.com/login/",
    ]
    rules = (
        Rule(LinkExtractor(
            allow='login',
        ), callback='do_login'),
        Rule(LinkExtractor(
            restrict_xpaths=('//div[contains(@class, "pinned-courses")]/div/div/div[contains(@class, "detail")]')
        ), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths=('//div[contains(@class, "levels")]'),
        ), callback='parse_level'),
    )

    def do_login(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': USER, 'password': PASSWORD},
        )

    def parse_level(self, response):
        item = MemriseItem()
        import ipdb; ipdb.set_trace()

