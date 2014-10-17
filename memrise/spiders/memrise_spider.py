from urlparse import urljoin
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from loginform import fill_login_form

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
    )

    def do_login(self, response):
        args, url, method = fill_login_form(response.url, response.body,
            USER, PASSWORD)
        return scrapy.FormRequest(url, method=method, formdata=args,
                callback=self.parse_dashboard)

    def parse_dashboard(self, response):
        # If the course has several level, scrape them
        pagination_selector = '//div[contains(@class, "title")]/a/@href'
        for url in response.xpath(pagination_selector).extract():
            yield scrapy.Request(urljoin('http://www.memrise.com', url), callback=self.parse_level)

    def parse_level(self, response):
        pagination_selector = '//div[contains(@class, "levels")]/a/@href'
        for url in response.xpath(pagination_selector).extract():
            yield scrapy.Request(urljoin('http://www.memrise.com', url), callback=self.parse_level)

        course = response.xpath('//h1[contains(@class, "course-name")]/text()').extract()[0]
        for sel in response.xpath('//div[contains(@class, "thing text-text")]'):
            item = MemriseItem()
            item['course'] = course
            item['item_id'] = sel.xpath('@data-thing-id').extract()[0]
            status = sel.xpath('div/div[contains(@class, "status")]/text()').extract()
            if not status:
                status = "not learnt"
            elif status == ["now"]:
                status = "now"
            elif status == ['in about a day']:
                status = [1, 'day']
            elif status == ['in about an hour']:
                status = [1, 'hour']
            elif status == ['in about a minute']:
                status = [1, 'minute']
            else:
                status = status[0].split()[1:]
                status[0] = int(status[0])
            item['status'] = status
            yield item
