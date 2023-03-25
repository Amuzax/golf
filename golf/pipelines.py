# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class GolfPipeline:
    def process_item(self, item, spider):
        return item

class DriverPipeline:
    def process_item(self, item, spider):
        # 指定の item を取得できなかった場合は破棄する
        if not item['loft']:
            raise DropItem('■ Missing Price! ■')
        # 指定の item を正しく取得できた場合は値を返す
        return item
    