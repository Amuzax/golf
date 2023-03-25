# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

def strip_yen(element):
    if element:
        return element.replace('¥', '')
    return element

def strip_comma(element):
    if element:
        return element.replace(',', '')
    return element

def convert_integer(element):
    if element:
        return int(element)
    return 0

def convert_float(element):
    if element:
        return float(element)
    return 0

def get_name(element):
    if element:
        return element.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').replace(']', '').split('/')[0]
    return element

def get_shaft(element):
    if element:
        return element.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').replace(']', '').split('/')[1]
    return element

def get_flex(element):
    if element:
        return element.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').replace(']', '').split('/')[2]
    return element

def get_loft(element):
    if element:
        return element.replace(' [', '/').replace(' フレックス：', '/').replace(' ロフト：', '/').replace(']', '').split('/')[3]
    return 0

class DriverItem(scrapy.Item):
    rank = scrapy.Field(
        input_processor = MapCompose(convert_integer),
        output_processor = TakeFirst()
    )
    maker = scrapy.Field(
        output_processor = TakeFirst()
    )
    name = scrapy.Field(
        input_processor = MapCompose(get_name),
        output_processor = TakeFirst()
    )
    shaft = scrapy.Field(
        input_processor = MapCompose(get_shaft),
        output_processor = TakeFirst()
    )
    flex = scrapy.Field(
        input_processor = MapCompose(get_flex),
        output_processor = TakeFirst()
    )
    loft = scrapy.Field(
        input_processor = MapCompose(get_loft, convert_float),
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        input_processor = MapCompose(strip_yen, strip_comma, convert_integer),
        output_processor = TakeFirst()
    )