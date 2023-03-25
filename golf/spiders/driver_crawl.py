import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
from golf.items import DriverItem
from scrapy.loader import ItemLoader

class DriverCrawlSpider(CrawlSpider):
    name = 'driver_crawl'
    allowed_domains = ['kakaku.com']
    start_urls = ['https://kakaku.com/golf/driver/ranking_6110/spec=103-21/']

    rules = (
        # 詳細ページを開く
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class,"rkgBoxHead")]/a'), callback='parse_item', follow=False),
        # 次のページを開く
        # Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"次へ")]')),
    )

    def parse_item(self, response):
        logging.info(response.url)

        loader = ItemLoader(item = DriverItem(), response = response)
        loader.add_xpath('rank', '//li[@class="ranking"]//span[@class="num"]/text()')
        loader.add_xpath('maker', '//li[@class="makerLabel"]/a/text()')
        loader.add_xpath('name', '//h2/text()')
        loader.add_xpath('shaft', '//h2/text()')
        loader.add_xpath('flex', '//h2/text()')
        loader.add_xpath('loft', '//h2/text()')
        loader.add_xpath('price', '//div[@class="priceWrap"]//span[@class="priceTxt"]/text()')
        yield loader.load_item()
