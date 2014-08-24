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
        course = response.xpath('//h1[contains(@class, "course-name")]/text()').extract()[0]
        for sel in response.xpath('//div[contains(@class, "thing text-text")]'):
            item = MemriseItem()
            item['course'] = course
            item['item_id'] = sel.xpath('@data-thing-id').extract()[0]
            status = sel.xpath('div/div[contains(@class, "status")]/text()').extract()
            if not status:
                status = "not learnt"
            elif status == ['in about a day']:
                status = [1, 'days']
            else:
                status = status[0].split()[1:]
                status[0] = int(status[0])
            item['status'] = status
            yield item
