import scrapy
import logging
from golf.items import DriverItem
from scrapy.loader import ItemLoader

class DriverSpider(scrapy.Spider):
    name = 'driver'
    allowed_domains = ['kakaku.com']
    start_urls = ['https://kakaku.com/golf/driver/ranking_6110/']

    def get_rank(self, rank):
        if rank:
            return int(rank)
        return rank
    
    def get_name(self, name):
        if name:
            return name.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').strip(']').split('/')[0]
        return name
    
    def get_shaft(self, shaft):
        if shaft:
            return shaft.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').strip(']').split('/')[1]
        return shaft

    def get_flex(self, flex):
        if flex.count('フレックス')>=1:
            if flex:
                return flex.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').strip(']').split('/')[2]
            return flex
        return 'UNKNOWN'
    
    def get_loft(self, loft):
        if loft.count('フレックス')>=1:
            if loft:
                return float(loft.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').strip(']').split('/')[3])
            return 0
        return float(loft.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').strip(']').split('/')[2])
    
    def get_price(self, price):
        if price:
            return int(price.replace('¥', '').replace(',', ''))
        return 0
    
    def parse(self, response):
        logging.info(response.url)

        lists = response.xpath('//div[contains(@class,"rkgBox noGraph")]')
        
        for list in lists:
            item = DriverItem()
            item['rank'] = self.get_rank(list.xpath('.//span[@class="rkgBoxNum"]//span[@class="num"]/text()').get())  # 同クラス内の get_rank メソッドで処理する
            item['maker'] = list.xpath('.//span[@class="rkgBoxNameMaker"]/text()').get()
            item['name'] = self.get_name(list.xpath('.//span[@class="rkgBoxNameItem"]/text()').get())
            item['shaft'] = self.get_shaft(list.xpath('.//span[@class="rkgBoxNameItem"]/text()').get())
            item['flex'] = self.get_flex(list.xpath('.//span[@class="rkgBoxNameItem"]/text()').get())
            item['loft'] = self.get_loft(list.xpath('.//span[@class="rkgBoxNameItem"]/text()').get())
            item['price'] = self.get_price(list.xpath('.//span[@class="price"]/a/text()').get())
            # item['price'] = list.xpath('.//a[@class="price"]/a/text()').get()  # price を取得できない実験用
            yield item
